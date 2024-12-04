from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_taggit.forms import TagWidget  # Import TagWidget for tags
from .models import CustomUser, Post, Comment
from django.forms import TextInput, Textarea
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'picture', 'bio')


class CustomUserChangeForm(UserChangeForm):
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Update your bio'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'picture', 'bio')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),
        }
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Add tags to form fields


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here'})
    )

    class Meta:
        model = Comment
        fields = ['content']
