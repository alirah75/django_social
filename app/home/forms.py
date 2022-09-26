from django import forms
from pyexpat import model

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


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostSearchForm(forms.Form):
    search = forms.CharField()
