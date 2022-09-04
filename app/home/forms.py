from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class CommentCreatedForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widget = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
