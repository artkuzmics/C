from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('posts',views.posts),
    path('posts/<int:pk>',views.post.as_view()),
    path('posts/<int:pk>/comments',views.comments),
    path('posts/<int:pk>/likes',views.likes),
    path('posts/<int:pk>/dislikes',views.dislikes),
    path('posts/topics/<str:topic>',views.filter.as_view()),
    path('posts/topics/<str:topic>/<str:status>',views.filter.as_view()),
    path('posts/topics/<str:topic>/<str:status>/<str:rank>',views.filter.as_view()),
]
