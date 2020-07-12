from . import views
from django.urls import path, include

urlpatterns = [
    path('create_t_up', views.create_t_up, name='create_t_up'),
    path('<int:team_up_id>/', views.detail, name='details'), 
    path('technology', views.technology, name='technology'), 
    path('joined_tups', views.joined_tups, name='joined_tups'),    
    # path('<int:product_id>/upvote', views.upvote, name='upvote'),
]