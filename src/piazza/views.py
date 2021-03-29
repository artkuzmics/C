import copy
import json
from .models import Post, Like, Dislike, Topic
from django.contrib.auth.models import User
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, TopicSerializer, DislikeSerializer
from rest_framework import status
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


@api_view(['GET','POST'])
def comments(request,id):
    '''
    Returns list of comments associated with a particular post and allows to create a new comment by an authorized user.
    '''
    # Post is retrieved by id.
    post = get_object_or_404(Post, id=id)
    # !!!! TRY
    if request.method == 'GET':
        # All comments associated with a post are retrieved.
        comments = post.comments.all()
        # The comments are serialized
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Check if post is live
        if post.islive:
            data = request.POST.copy()
            # Author's id and post's id is retrieved from the request and added to data
            data['post'] = post.id
            data['author'] = request.user.id
            # The data is serialized
            serializer = CommentSerializer(data=data)
            # Validate the data
            if serializer.is_valid():
                # If it is valid, save the data (create the comment)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Error if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Error if post is expired (POST method is disabled)
        return Response({'error':'post expired'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','PUT'])
def likes(request,id,reaction):
    post = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        serializer = LikeSerializer(post.likes.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if post.islive:
            if request.user.id == post.author_id.id:
                return Response({'error':'cannot like your own message'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            data = request.data.copy()
            data['post'] = post.id
            data['author'] = request.user.id
            try:
                dislike = Dislike.objects.get(post__id=post.id, author__username=request.user.username)
                dislike.delete()
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

        # Error if post is expired (POST method is disabled)
        return Response({'error':'post expired'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET','PUT'])
def dislikes(request,id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        serializer = DislikeSerializer(post.dislikes.all(), many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if post.islive:
            if request.user.id == post.author_id.id:
                return Response({'error':'cannot dislike your own message'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
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
        return Response({'error':'post expired'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
