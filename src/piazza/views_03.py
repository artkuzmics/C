import copy
import json
from .models import Post, Like, Dislike, Topic
from django.contrib.auth.models import User
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, TopicSerializer, DislikeSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

def sort_by_topic(posts, query):
    '''
    Sorts posts by topic (query) and produces activity vector based on number of likes and dislikes
    '''
    activity = []
    posts_by_topic = []
    for post in posts:
        # Topics are retrieved from each post
        topics = Topic.objects.filter(post=post.id)
        for topic in topics:
            # Each topic is compared with query
            if topic.topic.lower() == query.lower():
                # If matched, the post is added to the list and its activity (total number of likes and dislikes) is calculated and added to the activity vector.
                posts_by_topic.append(post)
                activity.append(post.likes.count()+post.dislikes.count())
    return posts_by_topic, activity

"""
class posts(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request):

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        if self.request.method == 'POST':
            data = json.loads(self.request.data)
            data['author_id'] = self.request.user.id
            kwargs["data"] = data
            return serializer_class(*args, **kwargs)
        return serializer_class(*args, **kwargs)
"""

class posts(APIView):
    '''
    Returns all posts and allows to create a new post.
    '''
    def get(self, request):
        # All posts are retrieved from database
        posts = Post.objects.all()
        # The posts are serialized
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # The data is retrieved from the request in JSON format
        data = request.data
        data = json.loads(data)
        # The ID of author is retrieved from the request and added to the data of the post
        data['author_id'] = request.user.id
        # The data is serialized
        serializer = PostSerializer(data=data)
        # Validate the data
        if serializer.is_valid():
            # If it is valid, save the data (create the post)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Error if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def post(request,id):
    '''
    Returns a post instance by id.
    '''
    if request.method == 'GET':
        # Post is retrieved by id.
        post = [get_object_or_404(Post, id=id)]

# !!!! TRY

        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)


class comments(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self, request):
        comments = Comment.objects.filter(post=self.kwargs['pk'])
        return comments

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        if self.request.method == 'POST':
            # The data is retrieved from the request in JSON format
            data = self.request.data.copy()
            # The ID of author is retrieved from the request and added to the data of the post
            data['post'] = self.kwargs['pk']
            data['author'] = self.request.user.id
            kwargs["data"] = data
            return serializer_class(*args, **kwargs)
        return serializer_class(*args, **kwargs)


class likes(UpdateAPIView, CreateModelMixin):
    serializer_class = LikeSerializer

    def get_queryset(self):
        likes = Like.objects.filter(post=self.kwargs['pk'], author=self.request.user.id)
        return likes

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        if self.request.method == 'PUT':
            # The data is retrieved from the request in JSON format
            data = self.request.data.copy()
            # The ID of author is retrieved from the request and added to the data of the post
            data['post'] = self.kwargs['pk']
            data['author'] = self.request.user.id
            kwargs["data"] = data
            return serializer_class(*args, **kwargs)
        return serializer_class(*args, **kwargs)

class dislikes(ListCreateAPIView):
    serializer_class = DislikeSerializer
    def get_queryset(self, request):
        likes = Like.objects.filter(post=self.kwargs['pk'])
        return likes

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        if self.request.method == 'POST':
            # The data is retrieved from the request in JSON format
            data = self.request.data.copy()
            # The ID of author is retrieved from the request and added to the data of the post
            data['post'] = self.kwargs['pk']
            data['author'] = self.request.user.id
            kwargs["data"] = data
            return serializer_class(*args, **kwargs)
        return serializer_class(*args, **kwargs)



@api_view(['GET'])
def topics(request,topic):
    if request.method == 'GET':
        posts = Post.objects.all()
        posts_by_topic, activity = sort_by_topic(posts, topic)
        serializer = PostSerializer(posts_by_topic, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def active(request,query):
    if request.method == 'GET':
        posts = Post.objects.all()
        posts_by_topic, activity = sort_by_topic(posts, query)
        max_value = max(activity)
        max_indices = [i for i, j in enumerate(activity) if j == max_value]
        active_topics = [posts_by_topic[i] for i in max_indices]
        serializer = PostSerializer(active_topics, many=True)
        return Response(serializer.data)
