from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from subscribers.models import NewsLetter
from .models import Post


class HomeView(generic.View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(is_featured=True)[:3]
        latests = Post.objects.order_by('-timestamp')[:3]
        context = {
            'object_list': posts,
            'latests': latests,
        }
        return render(self.request, 'posts/index.html', context)

    def post(self, request, *args ,**kwargs):
        email = request.POST.get('email')
        subscriber_email = NewsLetter()
        subscriber_email.email = email
        subscriber_email.save()
        messages.info(request, 'thanks for subscribing to our newsletter!')
        return redirect('posts:home')



class PostDetailView(generic.DetailView):
    template_name = 'posts/post.html'
    model = Post
    def get_context_data(self, *args,**kwargs):
        recent_posts = Post.objects.order_by('-timestamp').filter(is_featured=True)[:3]
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        # context['recent_posts'] = recent_posts
        context.update({
            'recent_posts': recent_posts
        })
        return context
