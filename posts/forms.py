from django import forms
from .models import *

class PostForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))

    class Meta:
        model = Post
        fields = ("content", "image",)

class CommentForm(forms.ModelForm):

    body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'add a comment...', 'rows':1}))

    class Meta:
        model = Comment
        fields = ("body",)

