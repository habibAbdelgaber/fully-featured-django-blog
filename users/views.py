from email import message
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.core.mail import send_mail

from .forms import ContactForm

class ContactView(FormView):
    form_class = ContactForm
    template_name = 'users/contact.html'
    def post(self, request):
        form = ContactForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            content = form.cleaned_data.get('message')

            message = f"""
                Hi i am, {username}. email: {email}
                -------------------------------------
                {content}
            """

            send_mail(
                subject=subject,
                message=message,
                recipient_list=['fromAdmin@gmail.com'],
                from_email=email,
            )

            return redirect('posts:home')
