from django import forms
from .models import Books


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'description']

class BookUpdateForm(forms.ModelForm):
    class Meta: 
        model = Books
        fields = ['title', 'description']

