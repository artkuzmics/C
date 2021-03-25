from rest_framework import generics, viewsets
from .models import Post, Like, Dislike, Topic
from django.contrib.auth.models import User
import copy
import json
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, TopicSerializer, DislikeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404

from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse


@api_view(['GET'])
def wall_by_topic(request,query):
    if request.method == 'GET':

        print('get')
        print(request.user)
        print(request.user.id)
        print(request.headers)

        posts = Post.objects.all()

        posts_by_topic = []
        for post in posts:
            topics = Topic.objects.filter(post=post.id)
            for topic in topics:
                print(topic.topic.lower(), query.lower())
                if topic.topic.lower() == query.lower():
                    posts_by_topic.append(post)

        serializer = PostSerializer(posts_by_topic, many=True)

        return Response(serializer.data)



@api_view(['GET','POST'])
def wall_posts(request):
    """
    List all code snippets, or create a new snippet.
    """

    if request.method == 'GET':

        print('get')
        print(request.user)
        print(request.user.id)
        print(request.headers)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':

        print('post')
        data = request.data
        data = json.loads(data)
        data['author'] = request.user.id

        print(data)
        serializer = PostSerializer(data=data)

        print(serializer)
        print(serializer.is_valid())
        print(serializer.errors)


        if serializer.is_valid():
            print('is_valid')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self,request):
        print(request.data)

"""

@api_view(['GET'])
def post(request,id):
    if request.method == 'GET':
        post = [get_object_or_404(Post, id=id)]
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

@api_view(['GET','POST'])
def comments(request,id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    comments_count = post.comments.count()
    print(comments_count)

    if request.method == 'GET':
        comment_serializer = CommentSerializer(comments, many=True)
        return Response(comment_serializer.data)

    elif request.method == 'POST':
        data = request.POST.copy()
        data['post'] = post.id
        data['author'] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def like(request,id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        serializer = LikeSerializer(post.likes.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['post'] = post.id
        data['author'] = request.user.id

        try:
            dislike = Dislike.objects.get(post__id=post.id, author__username=request.user.username)
            dislike.delete()
            print("dislike deleted")
        except Dislike.DoesNotExist:
            print("no dislike found")

        try:
            like = Like.objects.get(post__id=post.id, author__username=request.user.username)
            serializer = LikeSerializer(like, data=data)
        except Like.DoesNotExist:
            serializer = LikeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def dislike(request,id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        serializer = DislikeSerializer(post.dislikes.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['post'] = post.id
        data['author'] = request.user.id

        try:
            like = Like.objects.get(post__id=post.id, author__username=request.user.username)
            like.delete()
            print("like deleted")
        except Like.DoesNotExist:
            print("no like found")


        try:
            dislike = Dislike.objects.get(post__id=post.id, author__username=request.user.username)
            serializer = DislikeSerializer(dislike, data=data)
        except Dislike.DoesNotExist:
            serializer = DislikeSerializer(data=data)




        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
