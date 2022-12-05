from django import forms
from .models import TestSet, Comments, PostImage


class TestSetForm(forms.ModelForm):
    class Meta:
        model=TestSet
        fields = ['title', 'body',  'feature', 'tag', 'categories']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ('body', 'user')



class PostImageFrom(forms.ModelForm):

    class Meta:
        model=PostImage
        fields = ['image']
