from django import forms
from .models import Post, Comment




class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Leave your comment here...', 'rows': 2}))
    class Meta:
        model = Comment
        fields = ('content',)