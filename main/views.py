from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Comment
from django.contrib.auth.models import User
from django.http import JsonResponse
from accounts.models import UserProfile
from django.views import View
from .utils import log_book_view
# Create your views here.

def index(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'index.html', context)

def profile(request, username):
    profile = User.objects.get(username=username)
    return render(request, 'profile.html', {'profile': profile})

def book_view(request, slug):
    book = Book.objects.get(slug=slug)
    log_book_view(book=book, user=request.user)
    
    comments = Comment.objects.filter(book=book, parent=None).order_by('-created_at')
    follower = False
    if request.user.is_authenticated and request.user.userprofile in book.author.userprofile.followers.all():
        follower = True
    
    suggestions = Book.objects.all().exclude(id__in=[book.id])
    return render(request, 'book_view.html', {
        'book': book, 
        'suggestions': suggestions, 
        'follower': follower,
        'comments': comments
        })

def search_results(request):
    if request.method == "GET":
        q = request.GET.get('q')
        books = Book.objects.filter(title__icontains=q) | Book.objects.filter(description__icontains=q) | Book.objects.filter(author__userprofile__full_name__icontains=q) | Book.objects.filter(category__name__icontains=q)
        books = books.distinct()
        return render(request, 'search_result.html', {'q': q, 'books': books})
    return redirect('main:index')

@login_required
def toggle_follow(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id') 
        target_profile = get_object_or_404(UserProfile, user_id=user_id)
        follower_profile = get_object_or_404(UserProfile, user=request.user)

        if target_profile == follower_profile:
            return JsonResponse({'error': 'You cannot follow yourself.'}, status=400)
        
        if follower_profile in target_profile.followers.all():
            target_profile.followers.remove(follower_profile)
            status = "unfollowed"
        else:
            target_profile.followers.add(follower_profile)
            status = "followed"

        return JsonResponse({'status': status, 'followers_count': target_profile.followers.count(),'target_user': target_profile.full_name})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def toggle_like(request):
    book_id = request.POST.get('book_id')
    op = request.POST.get("op")
    target_book = get_object_or_404(Book, id=book_id)
    user = request.user
    if op == "like":
        if user in target_book.dislikes.all():
            target_book.dislikes.remove(user)
        if user in target_book.likes.all():
            target_book.likes.remove(user)
        else:
            target_book.likes.add(user)
        return JsonResponse({'status': 'success', 'likes': target_book.likes.count(), 'dislikes': target_book.dislikes.count()})
    elif op == "dislike":
        if user in target_book.likes.all():
            target_book.likes.remove(user)
        if user in target_book.dislikes.all():
            target_book.dislikes.remove(user)
        else:
            target_book.dislikes.add(user)
        return JsonResponse({'status': 'success', 'likes': target_book.likes.count(), 'dislikes': target_book.dislikes.count()})
    else:
        return JsonResponse({'error': 'Invalid request'})
    


class CommentView(View):
    def post(self, request, *args, **kwargs):
        comment = request.POST.get("comment", "").strip()
        book_id = int(request.POST.get("book_id"))
        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent = Comment.objects.filter(id=parent_id)
        else:
            parent = Comment.objects.none()

        user=request.user
        if not comment:
            return JsonResponse({"error": "Comment cannot be empty"}, status=400)
        target_book = Book.objects.get(id=book_id)
        new_comment = Comment.objects.create(user=user, content=comment, book=target_book)
        if parent.exists():
            new_comment.parent = parent.first()
            print("parent added.")
        new_comment.save()
        reply = False
        if new_comment.parent:
            reply = True
        response = {
            "message": "Comment submitted successfully", 
            "comment": comment,
            "comment_count": Comment.objects.filter(book=target_book).count(),
            "username": user.username,
            "profile_img": user.userprofile.profile_picture.url,
            "time": "Just now",
            "comment_id": new_comment.id,
            "reply":reply,
            "parent_id": parent_id,
            "book_id": book_id
            }
        return JsonResponse(response)

def delete_comment(request, comment_id):
    if request.method == "GET":
        target_comment = Comment.objects.get(id=comment_id)
        if target_comment.user != request.user:
            return JsonResponse({'error': "You can't delete others comment."}, status=404)
        target_comment.delete()
        return JsonResponse({
            "success": "Comment deleted.",
            "comment_id": comment_id
        })