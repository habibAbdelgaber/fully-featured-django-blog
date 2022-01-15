from django import forms



class ContactForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Your Name...'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Your e-mail address'
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your subject'
    }))
    message = forms.CharField(max_length=250, widget=forms.Textarea(attrs={
        'placeholder': 'Write a message',
        'rows': 3
    }))