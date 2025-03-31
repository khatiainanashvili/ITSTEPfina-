from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_blog/', views.add_blog, name='add_blog'), 
    path('blog/<int:id>/', views.blog_details, name='blog_detail'),
    path('blog/<int:id>/update/', views.update_blog, name='update_blog'),
    path('blog/<int:id>/delete/', views.delete_blog, name='delete_blog'),
    path('profile/', views.profile, name='profile'),
     path('profile/update/', views.update_profile, name='update_profile'),
     path('comment/<int:id>/delete/', views.delete_comment, name='delete_comment'),
    path('author/<int:id>/', views.author_profile, name='author_profile'),
]
