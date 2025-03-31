from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

]



