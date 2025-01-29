from django.shortcuts import render
from .models import Book
from django.contrib.auth.models import User
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
    suggestions = Book.objects.all().exclude(id__in=[book.id])
    return render(request, 'book_view.html', {'book': book, 'suggestions': suggestions})