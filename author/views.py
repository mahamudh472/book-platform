from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main.models import Book, User, Comment, BookView, Booktranslation
from django.contrib import messages
from .forms import BookUploadForm, NewsForm, NewsImageFormSet, AudioForm, TranslationForm
import base64
from django.core.files.base import ContentFile
from main.utils import get_last_n_days_data, year_specific_data

# Create your views here.
@login_required(login_url='accounts:login')
def author_dashboard(request):
    return render(request, 'author/admin_dashboard.html')

@login_required(login_url='accounts:login')
def author_content(request):
    return render(request, 'author/admin_content.html')

@login_required(login_url='accounts:login',)
def author_analytics(request):
    views = get_last_n_days_data(BookView, 90, user=request.user)
    # days = request.GET.get('days', None)
    # year = request.GET.get('year', None)
    # if days:
    #     views = get_last_n_days_data(BookView, int(days), user=request.user)
    # elif year:
    #     views = year_specific_data(BookView, int(year))

    context = {
        'views': views
    }
    return render(request, 'author/admin_analytics.html', context)

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
def content_details(request, slug):
    book = Book.objects.get(slug=slug)
    context = {
        'book': book
    }
    return render(request, 'author/content_details.html', context)

@login_required(login_url='accounts:login')
def content_analytics(request, slug):
    book = Book.objects.get(slug=slug)
    context = {
        'book': book
    }
    return render(request, 'author/content_analytics.html', context)

@login_required(login_url='accounts:login')
def content_comments(request, slug):
    book = Book.objects.get(slug=slug)
    context = {
        'book': book
    }
    return render(request, 'author/content_comments.html', context)

@login_required(login_url='accounts:login')
def content_copyright(request, slug):
    book = Book.objects.get(slug=slug)
    context = {
        'book': book
    }
    return render(request, 'author/content_copyright.html', context)

@login_required(login_url='accounts:login')
def content_translate(request, slug):
    book = Book.objects.get(slug=slug)
    if request.method == "POST":
        form = TranslationForm(request.POST)
        if form.is_valid():
            translation = form.save(commit=False)
            translation.book = book
            translation.save()
            messages.success(request, 'Translation added to book')
        else:
            print(form.errors)
            messages.error(request, 'Invalid response')
    form = TranslationForm()
    context = {
        'book': book,
        'form': form
    }
    return render(request, 'author/content_translate.html', context)


def get_translation(request, book_id, translation_id):
    if translation_id == 0:
        book = Book.objects.get(id=book_id)
        context = {
            'translated_title': book.title,
            'translated_description': book.description,
            'translated_content': book.content
        }
    else:
        translation = Booktranslation.objects.get(id=translation_id)
        context = {
            'translated_title': translation.translated_title,
            'translated_description': translation.translated_description,
            'translated_content': translation.translated_content
        }
    return JsonResponse(context)


@login_required(login_url='accounts:login')
def content_audio(request, slug):
    book = Book.objects.get(slug=slug)
    if request.method == "POST":
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio = form.save(commit=False)
            audio.book = book
            audio.save()
            messages.success(request, "Audio added to book.")
        else:
            messages.error(request, 'Invalid files')
    form = AudioForm()
    context = {
        'book': book,
        'form': form
    }
    return render(request, 'author/content_audio.html', context)

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

@login_required(login_url='accounts:login')
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        formset = NewsImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            images = formset.save(commit=False)
            for image in images:
                image.news = news
                image.save()
            messages.success(request, "News added")
            return redirect('main:index')
        else:
            messages.error(request, "News creation faild")
            return redirect('main:index')
    else:
        form = NewsForm()
        formset = NewsImageFormSet()
        return render(request, 'author/create_news.html', {'form': form, 'formset': formset})
    
@login_required(login_url='accounts:login')
def change_visibility(request, book_id, status):
    book = Book.objects.get(id=book_id)
    if book.author == request.user:
        book.status = status
        book.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

