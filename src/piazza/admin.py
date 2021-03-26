from django.contrib import admin
from .models import Post, Comment, Like, Dislike, Topic

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('body','author_id','timestamp')
    list_filter = ('author_id','timestamp')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_id','created','post')
    list_filter = ('author_id','post')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author_id','post')
    list_filter = ('author_id','post')

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('author_id','post')
    list_filter = ('author_id','post')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id','post','topic')
