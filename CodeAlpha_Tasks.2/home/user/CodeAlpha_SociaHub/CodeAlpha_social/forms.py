from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Post, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar", "location"]

        widgets = {
            "bio": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Tell people about yourself..."
            }),
            "location": forms.TextInput(attrs={
                "placeholder": "City, Country"
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]

        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What's happening?"
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.TextInput(attrs={
                "placeholder": "Write a comment..."
            })
        }