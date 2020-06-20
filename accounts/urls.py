from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('showdata', views.showuserdata, name='showdata'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
]
