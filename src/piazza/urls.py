from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.wall_posts),
    path('<str:query>',views.wall_by_topic),
    path('<int:id>',views.post),
    path('<int:id>/comments',views.comments),
    path('<int:id>/like',views.like),
    path('<int:id>/dislike',views.dislike),
]
# Create your tests here.
