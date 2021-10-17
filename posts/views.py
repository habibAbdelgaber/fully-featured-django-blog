from django.shortcuts import render
from django.views import generic
from .models import Post


class HomeView(generic.View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(is_featured=True)[:3]
        # cat = posts.category()
        context = {
            'object_list': posts,
            # 'cat': cat,
        }
        return render(self.request, 'posts/index.html', context)
