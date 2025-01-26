from django.shortcuts import render
from .models import Book
# Create your views here.

def index(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'index.html', context)

def profile(request):
    return render(request, 'profile.html')

def book_view(request, slug):
    book = Book.objects.get(slug=slug)
    book.views += 1
    book.save()
    suggestions = Book.objects.all()
    return render(request, 'book_view.html', {'book': book, 'suggestions': suggestions})