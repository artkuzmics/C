from rest_framework import serializers
from .models import Post, Comment, Like, Dislike, Topic

TOPICS = ('health', 'sport', 'politics', 'tech')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('post','topic')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author','author_id','body','post','created')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('author','author_id','post')

class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ('author','author_id','post')

class PostSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True, required=False)
    likes = LikeSerializer(many=True, read_only=True, required=False)
    dislikes = DislikeSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Post
        fields = ('id','author','author_id','title','body','timestamp','expiration','islive','topics','comments','likes','dislikes')

    def create(self, validated_data):
        topics = validated_data.pop('topics')
        post = Post.objects.create(**validated_data)

        for topic in topics:
            if dict(topic)['topic'].lower() in TOPICS:
                Topic.objects.create(
                            post=post,
                            **topic
                            )
        return post
