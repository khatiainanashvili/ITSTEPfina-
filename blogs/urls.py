from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_book/', views.add_book, name='add_book'), 
    path('book/<int:id>/', views.blog_details, name='blog_detail'),
    path('update_book/<int:id>/', views.update_book, name='update_book'),
    path('delete_blog/<int:id>/', views.delete_blog, name='delete_blog'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('author/<int:id>/', views.author_profile, name='author_profile'),
]
