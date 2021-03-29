from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('posts',views.posts),
    path('posts/<int:id>',views.post),
    path('posts/<int:id>/comments',views.comments),
    path('posts/<int:id>/likes',views.likes),
    path('posts/<int:id>/dislikes',views.dislikes),
    path('posts/topics/<str:topic>',views.topics),
    #path('posts/topics/<str:topic>/active',views.topics_active),
    #path('posts/topics/<str:topic>/expired',views.topics_active),
    #path('posts/topics/<str:topic>/active/best-ranked',views.topics_active_bestranked),
]
