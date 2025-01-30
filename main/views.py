from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book
from django.contrib.auth.models import User
from django.http import JsonResponse
from accounts.models import UserProfile
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
    book.views += 1
    book.save()
    follower = False
    if request.user.userprofile in book.author.userprofile.followers.all():
        follower = True
    
    suggestions = Book.objects.all().exclude(id__in=[book.id])
    return render(request, 'book_view.html', {'book': book, 'suggestions': suggestions, 'follower': follower})

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