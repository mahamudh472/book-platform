from django import forms
from main.models import Book
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
