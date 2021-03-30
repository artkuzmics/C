import copy
import json
from .models import Post, Like, Dislike, Topic
from django.contrib.auth.models import User
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, TopicSerializer, DislikeSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

class post(ListAPIView):
    '''
    Returns a post instance by id.
    '''
    serializer_class = PostSerializer
    def get_queryset(self):
        posts = Post.objects.filter(id=self.kwargs['pk'])
        return posts

class filter(ListAPIView):
    '''
    Filter posts by topic, status and top-ranked activity (likes+dislikes).
    '''
    serializer_class = PostSerializer

    def get_queryset(self):
        def best_ranked(posts):
            activity = [post.likes.count()+post.dislikes.count() for post in posts]
            indices = [i for i, j in enumerate(activity) if j == max(activity)]
            return [posts[i] for i in indices]

        topic = self.kwargs.get("topic")
        status = self.kwargs.get("status")
        rank = self.kwargs.get("rank")
        posts = Post.objects.filter(topics__topic=topic)

        if status != None and status !='best-ranked':
            if status == "active":
                status=True
            elif status == "expired":
                status=False
            else:
                raise Error
            posts = [post for post in posts if post.islive == status]
            if rank == 'best-ranked':
                best_ranked(posts)
            return posts

        elif status == 'best-ranked':
            best_ranked(posts)

        return posts


@api_view(['GET','POST'])
def posts(request):
    '''
    Returns all posts and allows to create a new post.
    '''
    if request.method == 'GET':
        # All posts are retrieved from database
        posts = Post.objects.all()
        # The posts are serialized
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
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

@api_view(['GET','POST'])
def comments(request,pk):
    '''
    Returns list of comments associated with a particular post and allows to create a new comment by an authorized user.
    '''
    # Post is retrieved by id.
    post = get_object_or_404(Post, id=pk)
    # !!!! TRY
    if request.method == 'GET':
        # All comments associated with a post are retrieved.
        comments = post.comments.all()
        # The comments are serialized
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.POST.copy()
        # Author's id and post's id is retrieved from the request and added to data
        data['post'] = post.id
        data['author_id'] = request.user.id
        # The data is serialized
        serializer = CommentSerializer(data=data)
        # Validate the data
        if serializer.is_valid():
            # If it is valid, save the data (create the comment)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Error if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def likes(request,pk):

    post = get_object_or_404(Post, id=pk)

    if request.method == 'GET':
        serializer = LikeSerializer(post.likes.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user.id == post.author_id.id:
            return Response({'error':'cannot like your own message'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        data = request.data.copy()
        data['post'] = post.id
        data['author_id'] = request.user.id
        try:
            dislike = Dislike.objects.get(post__id=post.id, author_id__username=request.user.username)
            dislike.delete()
        except Dislike.DoesNotExist:
            pass
        try:
            like = Like.objects.get(post__id=post.id, author_id__username=request.user.username)
            serializer = LikeSerializer(like, data=data)
        except Like.DoesNotExist:
            serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def dislikes(request,pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'GET':
        serializer = DislikeSerializer(post.dislikes.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user.id == post.author_id.id:
            return Response({'error':'cannot dislike your own message'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        data = request.data.copy()
        data['post'] = post.id
        data['author_id'] = request.user.id
        try:
            like = Like.objects.get(post__id=post.id, author_id__username=request.user.username)
            like.delete()
            print("like deleted")
        except Like.DoesNotExist:
            print("no like found")
        try:
            dislike = Dislike.objects.get(post__id=post.id, author_id__username=request.user.username)
            serializer = DislikeSerializer(dislike, data=data)
        except Dislike.DoesNotExist:
            serializer = DislikeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
