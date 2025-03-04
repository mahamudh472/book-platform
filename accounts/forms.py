from django import forms
from .models import UserProfile

class profileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['full_name', 'bio', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'p-2 rounded border w-full'}),
            'bio': forms.Textarea(attrs={'class': 'p-2 rounded border w-full'}),
            'profile_picture': forms.FileInput(attrs={'class': 'p-2 rounded border w-full'})
        }
