from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Comment, News, History, Collection, ReadingList, Notification
from django.contrib.auth.models import User
from django.http import JsonResponse
from accounts.models import UserProfile
from django.views import View
from .utils import log_book_view, create_notification
from django.utils import timezone, html
from collections import defaultdict
from django.contrib import messages
# Create your views here.

def index(request):
    context = {}
    path_info = request.META.get('PATH_INFO')
    if path_info == "/trending":
        books = Book.public_objects.all().order_by('-views')
        context['page'] = "Trending"
    elif path_info == "/recent":
        books = Book.public_objects.all().order_by('-published_date')
        context['page'] = "Recent"
    elif path_info == "/popular":
        books = Book.public_objects.all().order_by('-views')
        context['page'] = "Polular"
    else:
        books = Book.public_objects.all().order_by('?')
        context['page'] = "Recommended"
    context['books'] = books
    if request.user.is_authenticated:
        context['following'] = request.user.userprofile.following.all()[:3]
    return render(request, 'main/index.html', context)

from accounts.forms import profileForm
def profile(request, username):
    
    profile = User.objects.get(username=username)
    context = {'profile': profile}
    if request.user.username == username:
        if request.method == "POST":
            form = profileForm(request.POST, request.FILES, instance=profile.userprofile)
            if form.is_valid():
                form.save()
                return redirect(request.META.get('HTTP_REFERER', '/fallback-url/'))
        form = profileForm(request.POST or None, request.FILES or None, instance=profile.userprofile)
        context['form'] = form
    return render(request, 'main/profile.html', context)


def subscriptions(request):

    return render(request, 'main/subscriptions.html')

@login_required(login_url='accounts:login')
def collections(request):
    if request.method == "POST":
        collection_name = request.POST.get('collection_name')
        collection, created = Collection.objects.get_or_create(
            user=request.user,
            name=collection_name
        )
        if created:
            messages.success(request, 'Collection added')
        else:
            messages.error(request, "Collection alreay exists.")
        return redirect('main:collections')
    return render(request, 'main/collections.html')

def delete_collection(request, collection_id):
    collection = Collection.objects.filter(user=request.user, id=collection_id)
    if collection.exists():
        collection.first().delete()
        messages.success(request, 'Collection deleted.')
    else:
        messages.error(request, 'Collection not found.')
    return redirect('main:collections')

def collection(request, collection_name):
    coll = Collection.objects.filter(name=collection_name, user=request.user)
    if coll.exists():
        return render(request, 'single_collection.html', {'collection': coll.first()})
    else:
        messages.error(request, "Collection not found.")
        return redirect(request.META.get('HTTP_REFERER', '/fallback-url/'))

def add_to_collection(request, slug, collection_name):
    book = Book.public_objects.get(slug=slug)
    coll = Collection.objects.filter(user=request.user, name=collection_name)
    if coll.exists():
        obj, created =ReadingList.objects.get_or_create(
            collection=coll.first(),
            book=book
        )
        if created:
            messages.success(request, f"Book add to {coll.first().name}")
        else:
            messages.error(request, "Book already in this collection")
    else:
        messages.error(request, 'Failed adding in collection')
    return redirect(request.META.get('HTTP_REFERER', '/fallback-url/'))

def remove_from_collection(request, slug, collection_name):
    book = Book.public_objects.get(slug=slug)
    coll = Collection.objects.filter(user=request.user, name=collection_name)
    if coll.exists():
        obj = ReadingList.objects.get(collection=coll.first(), book=book)
        if obj:
            obj.delete()
            messages.success(request, f"Book removed from {coll.first().name}")
        else:
            messages.error(request, "Book not in collection")
    else:
        messages.error(request, 'Failed removing book from collection')
    return redirect(request.META.get('HTTP_REFERER', '/fallback-url/'))


def book_view(request, slug):
    book = Book.public_objects.get(slug=slug)
    user = request.user if request.user.is_authenticated else None
    log_book_view(book=book, user=user)

    # Add to history
    if request.user.is_authenticated:
        history, created = History.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={'updated_at': timezone.now()}
        )

    comments = Comment.objects.filter(book=book, parent=None).order_by('-created_at')
    follower = False
    if request.user.is_authenticated and request.user.userprofile in book.author.userprofile.followers.all():
        follower = True
    
    suggestions = Book.public_objects.all().exclude(id__in=[book.id])
    return render(request, 'main/book_view.html', {
        'book': book, 
        'suggestions': suggestions, 
        'follower': follower,
        'comments': comments
        })

def search_results(request):
    if request.method == "GET":
        q = request.GET.get('q')
        books = Book.public_objects.filter(title__icontains=q) | Book.public_objects.filter(description__icontains=q) | Book.public_objects.filter(author__userprofile__full_name__icontains=q) | Book.public_objects.filter(category__name__icontains=q)
        books = books.distinct()
        return render(request, 'main/search_result.html', {'q': q, 'books': books})
    return redirect('main:index')

@login_required(login_url='accounts:login')
def history(request):
    histories = History.objects.filter(user=request.user).order_by('-updated_at')

    # Get current date and yesterday's date
    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)

    # Group histories by date
    history_dict = defaultdict(list)

    for history in histories:
        history_date = history.updated_at.date()
        if history_date == today:
            history_dict["Today"].append(history)
        elif history_date == yesterday:
            history_dict["Yesterday"].append(history)
        else:
            history_dict[history_date.strftime("%B %d, %Y")].append(history)

    return render(request, 'main/history.html', {'history_dict': dict(history_dict)})

def clear_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    messages.error(request, 'Notifications cleared.')
    return redirect(request.META.get('HTTP_REFERER', '/fallback-url/'))


def mark_all_as_read(request):
    noti = Notification.objects.filter(user=request.user, is_read=False)
    for item in noti:
        item.is_read = True
        item.save()
    return redirect(request.META.get('HTTP_REFERER', '/fallback-url/'))


@login_required(login_url='accounts:login')
def continue_reading(request):
    histories = History.objects.filter(user=request.user).order_by('-updated_at')
    if histories.exists():
        his = histories.first()
        if his.book:
            return redirect('main:book_view', his.book.slug)
    messages.error(request, html.format_html("You haven't read anything yet."))
    return redirect(request.META.get('HTTP_REFERER', '/fallback-url/'))

@login_required(login_url='accounts:login')
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
            create_notification(target_profile.user, f"{follower_profile.full_name} followed you.")

        return JsonResponse({'status': status, 'followers_count': target_profile.followers.count(),'target_user': target_profile.full_name})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='accounts:login')
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
            if user != target_book.author: 
                create_notification(target_book.author, f"{user.userprofile.full_name} liked your book {target_book.title}")
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
        target_book = Book.public_objects.get(id=book_id)
        new_comment = Comment.objects.create(user=user, content=comment, book=target_book)
        if parent.exists():
            new_comment.parent = parent.first()
            print("parent added.")
        new_comment.save()
        reply = False
        if new_comment.parent:
            reply = True
            create_notification(new_comment.parent.user, f"{user.userprofile.full_name} replied to your comment.")
        if request.user != target_book.author:
            create_notification(target_book.author, f"{user.userprofile.full_name} commentent on your book.")
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
    
def news_cast(request):
    news = News.objects.all()
    return render(request, 'main/newscast.html', {'news': news})

def news(request):
    return render(request, 'main/news.html')