from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from tinymce import HTMLField

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField()
    description = HTMLField('content', blank=True, null=True)
    img = models.ImageField(upload_to='img/images/',blank=True, null=True)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    previous_post = models.ForeignKey('self', blank=True, null=True, related_name='previous', on_delete=models.SET_NULL)
    next_post = models.ForeignKey('self', blank=True, null=True, related_name='next', on_delete=models.SET_NULL)


    def __str__(self):
        return str(self.title)

    
    @property
    def get_comment_count(self):
        # comment_count = self.comment_set.all().count()
        # return comment_count
        return self.comment_set.all().count()

    @property
    def get_view_count(self):
        # comment_count = self.postview_set.all().count()
        # return comment_count
        return self.postview_set.all().count()

    # @property
    # def get_view_count(self):
    #     # comment_count = self.postview_set.all().count()
    #     # return comment_count
    #     return Post.objects.filter(comment__post=comment).count()
        
    @property
    def get_like_count(self):
        # comment_count = self.postlike_set.all().count()
        # return comment_count
        return self.postlike_set.all().count()

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    # def get_absolute_comment_url(self):
    #     return reverse('posts:detail', kwargs={'slug': self.slug, 'pk': self.comment.pk})
    
    
    def get_like_url(self):
        return reverse('posts:like', kwargs={'slug': self.slug})

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class PostView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name



