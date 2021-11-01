from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from subscribers.models import NewsLetter
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from .models import Post, PostLike, PostView


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
    form = CommentForm

    def get_object(self):
        obj = super(PostDetailView, self).get_object()
        if self.request.user.is_authenticated:
             PostView.objects.get_or_create(
            user=self.request.user,
            post=obj
        )

        return obj

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = self.request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('posts:detail', kwargs={'slug': post.slug}))


    def get_context_data(self, *args,**kwargs):
        recent_posts = Post.objects.order_by('-timestamp').filter(is_featured=True)[:3]
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        # context['recent_posts'] = recent_posts
        context.update({
            'recent_posts': recent_posts,
            'form': self.form
        })
        return context

@login_required
def get_post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = PostLike.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('posts:detail', slug=slug)
    PostLike.objects.create(
        user=request.user,
        post=post,
    )
    return redirect('posts:detail', slug=slug)