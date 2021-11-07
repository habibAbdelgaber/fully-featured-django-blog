from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('detail/<slug>/', views.PostDetailView.as_view(), name='detail'),
    path('detail/<slug>/like/', views.get_post_like, name='like')
]