from django import forms
from django.forms import inlineformset_factory
from main.models import Book, News, NewsImage, AudioBook
from django_ckeditor_5.widgets import CKEditor5Widget

class BookUploadForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget())
    class Meta:
        model = Book
        fields = ['thumbnail', 'title', 'description', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'description': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'content': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
            'category': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
        }

class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = News
        fields = ['title', 'category', 'description', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'description': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'content': forms.Textarea(attrs={'class': 'w-full border p-2 rounded'}),
            'category': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
        }

class NewsImageForm(forms.ModelForm):
    class Meta:
        model = NewsImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'w-full border p-2 rounded'}),
        }

NewsImageFormSet = inlineformset_factory(News, NewsImage, form=NewsImageForm, extra=3)

class AudioForm(forms.ModelForm):

    class Meta:
        model = AudioBook
        fields = ['language','narrator', 'file']
        widgets = {
            'language': forms.TextInput(attrs={'class': 'w-full border p-2 rounded mb-2'}),
            'narrator': forms.TextInput(attrs={'class': 'w-full border p-2 rounded mb-2'}),
            'file': forms.ClearableFileInput(attrs={'class': 'w-full border p-2 rounded' , 'accept': 'audio/*'})
        }
        