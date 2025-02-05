from django import forms
from main.models import Book
from django_ckeditor_5.widgets import CKEditor5Widget

class BookUploadForm(forms.ModelForm):
    contnet = forms.CharField(widget=CKEditor5Widget)
    class Meta:
        model = Book
        fields = ['thumbnail', 'title', 'description', 'content', 'category']

