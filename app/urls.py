from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('feed/', views.feed, name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('user/<str:username>/', views.profile, name='profile'),
    path('explore/', views.explore, name='explore'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]