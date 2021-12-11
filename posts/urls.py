from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search, name='search'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/create', views.CreatePostView.as_view(), name='post-create'),
    path('posts/detail/<slug>/', views.PostDetailView.as_view(), name='detail'),
    path('posts/detail/<slug>/update/', views.PostUpdateView.as_view(), name='update-post'),
    path('posts/detail/<slug>/delete/', views.PostDeleteView.as_view(), name='delete-post'),
    path('posts/detail/<slug>/like/', views.get_post_like, name='like')
]