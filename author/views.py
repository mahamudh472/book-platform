from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import Book, User, Comment
from django.contrib import messages
from .forms import BookUploadForm
import base64
from django.core.files.base import ContentFile

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
    comments = Comment.objects.filter(book__author=request.user)
    context = {
        'comments': comments
    }
    return render(request, 'author/admin_community.html', context)

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
        form = BookUploadForm(request.POST, request.FILES)

        # Handle cropped image
        cropped_image_data = request.POST.get("cropped_thumbnail")
        if cropped_image_data:
            format, imgstr = cropped_image_data.split(';base64,')  
            ext = format.split('/')[-1]  

            # Convert Base64 to an image file
            image_data = ContentFile(base64.b64decode(imgstr), name=f"cropped_thumbnail.{ext}")
            form.instance.thumbnail = image_data  # Set it to the form

        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, "Book published")
            return redirect("main:index")
    form = BookUploadForm(request.POST or None, request.FILES or None)
    return render(request, "author/write_book.html", {"form": form})
