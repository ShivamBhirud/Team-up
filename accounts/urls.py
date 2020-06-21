from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('user_profile', views.showuserdata, name='user_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_profile_page', views.show_profile_page, name='show_profile_page'),
]
