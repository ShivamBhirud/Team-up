from . import views
from django.urls import path, include

urlpatterns = [
    path('create_t_up', views.create_t_up, name='create_t_up'),
    path('<int:team_up_id>/', views.detail, name='details'), 
    path('category/<str:category>/', views.tup_category, name='category'),
    path('join_tup/<int:recruiter>/', views.join_tup, name='join_tup'), 
    path('show_teamup_details', views.show_teamup_details, name='show_teamup_details'), 
    path('requests', views.requests, name='requests'),
    path('notifications', views.notifications, name='notifications'),
    path('application', views.application, name='application'),
    path('user_profile/<int:user>/', views.user_profile, name='user_profile'),
    path('user_teamups', views.user_teamups, name='user_teamups'),
    path('remove_teammate/<int:adv>/', views.remove_teammate, name='remove_teammate'),
    # path('<int:product_id>/upvote', views.upvote, name='upvote'),
]