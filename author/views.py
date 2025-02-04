from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import Book, User
from django.contrib import messages

# Create your views here.
@login_required(login_url='accounts:login')
def author_dashboard(request):
    return render(request, 'author/admin_dashboard.html')

@login_required(login_url='accounts:login')
def author_content(request):
    return render(request, 'author/admin_content.html')

@login_required(login_url='accounts:login')
def author_analytics(request):
    return render(request, 'author/admin_analytics.html')

@login_required(login_url='accounts:login')
def author_community(request):
    return render(request, 'author/admin_community.html')

@login_required(login_url='accounts:login')
def author_earn(request):
    return render(request, 'author/admin_earn.html')

@login_required(login_url='accounts:login')
def author_copyright(request):
    return render(request, 'author/admin_copyright.html')

@login_required(login_url='accounts:login')
def content_details(request):
    return render(request, 'author/content_details.html')

@login_required(login_url='accounts:login')
def content_analytics(request):
    return render(request, 'author/content_analytics.html')

@login_required(login_url='accounts:login')
def content_comments(request):
    return render(request, 'author/content_comments.html')

@login_required(login_url='accounts:login')
def content_copyright(request):
    return render(request, 'author/content_copyright.html')

@login_required(login_url='accounts:login')
def content_translate(request):
    return render(request, 'author/content_translate.html')


@login_required(login_url='accounts:login')
def write_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('book_content')
        thumbnail = request.FILES.get('thumbnail')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        print(request.POST)
        print(request.FILES)
        if not title:
            pass
        if not description:
            pass
        if not content:
            pass
        if not thumbnail:
            pass
        if not category:
            pass
        if not tags:
            pass
        book = Book.objects.create(
            title=title,
            description=description,
            content=content,
            author=request.user,
        )
        if thumbnail:
            book.thumbnail = thumbnail
        book.save()
        messages.success(request, "Book published successfully.")

        return redirect('author:write_book')


    return render(request, 'author/write_book.html')
