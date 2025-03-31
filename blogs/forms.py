from django import forms
from .models import Author, Blogs, User


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['title', 'description']

class BookUpdateForm(forms.ModelForm):
    class Meta: 
        model = Blogs
        fields = ['title', 'description']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['avatar']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username'] 

