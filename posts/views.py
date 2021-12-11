from django.contrib import messages
from django.forms.models import modelform_factory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from subscribers.models import NewsLetter
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, PostForm
from .models import Post, PostLike, PostView
from django.core.paginator import Paginator


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


class PostListView(generic.ListView):
    model = Post
    template_name = 'posts/blog.html'
    paginate_by = 3

    def get_context_data(self, *args,**kwargs):
        recent_posts = Post.objects.order_by('-timestamp').filter(is_featured=True)[:3]
        category_count = Post.objects.values('categories__name').annotate(Count('categories__name'))
        tag_count = Post.objects.values('tags__name').annotate(Count('tags__name'))
        print(category_count)
        context = super(PostListView, self).get_context_data(*args,**kwargs)
        # context['recent_posts'] = recent_posts
        context.update({
            'recent_posts': recent_posts,
            'categories': category_count,
            'tags': tag_count
        })
        return context


class CreatePostView(generic.CreateView):
    model = Post
    form_class = PostForm
    # fields = ['author', 'title', 'slug', 'content', 'categories', 'tags', 'is_featured', 'img']
    # success_url = '/'

    def get_success_url(self):
        messages.success(self.request, 'the post was created successfully!')
        return reverse('posts:detail', args=[self.object.slug])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'create'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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
        category_count = Post.objects.values('categories__name').annotate(Count('categories__name'))
        tag_count = Post.objects.values('tags__name').annotate(Count('tags__name'))
        print(category_count)
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        # context['recent_posts'] = recent_posts
        context.update({
            'recent_posts': recent_posts,
            'categories': category_count,
            'tags': tag_count,
            'form': self.form
        })
        return context



class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    # fields = ['author', 'title', 'slug', 'content', 'categories', 'tags', 'is_featured', 'img']
    # success_url = '/'

    def get_success_url(self):
        messages.success(self.request, 'the post was update successfully!')
        return reverse('posts:detail', args=[self.object.slug])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Update'
        return context


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'posts/post.html'
    def get_success_url(self):
        messages.error(self.request, 'the post was deleted successfully!')
        return reverse('posts:home')





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


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('query')
    if query:
        posts = queryset.filter(Q(title__icontains=query)|Q(content__icontains=query))
    context = {'posts': posts}
    return render(request, 'posts/search.html', context)