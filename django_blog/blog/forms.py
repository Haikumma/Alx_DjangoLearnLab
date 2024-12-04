from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_taggit.forms import TagWidget  # Import TagWidget for tags
from .models import CustomUser, Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    picture = forms.ImageField()
    bio = forms.Textarea()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'picture', 'bio')  


class CustomUserChangeForm(UserChangeForm):
    bio = forms.CharField(max_length=500)  

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'picture', 'bio')       

class PostForm(forms.ModelForm):
    tags = forms.CharField(widget=TagWidget(), required=False)  # Tag input field

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Add tags to form fields
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = TaggableManager()  # Adding taggable manager to handle tags

    def __str__(self):
        return self.title
