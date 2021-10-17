from django.contrib import admin
from .models import Post, Comment, PostView, PostLike, Category, Tag

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(PostLike)
admin.site.register(Category)
admin.site.register(Tag)
