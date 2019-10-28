from django import forms
from .models import Post, Comment
from django.db import models
from django.contrib.auth.models import User



class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment here!!', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = ['content',]
