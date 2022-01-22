from django import forms
from django.forms import widgets
from .models import Post, Comment

from tinymce import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'post title...'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'placeholder': 'Write a post...',
        'class': 'mt-1',
        'rows': 5
        }))


    description = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'description', 'categories', 'tags', 'is_featured', 'previous_post', 'img']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'categories': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Leave your comment here...', 'rows': 2}))
    class Meta:
        model = Comment
        fields = ('content',)



