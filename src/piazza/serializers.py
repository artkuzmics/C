from rest_framework import serializers
from .models import Post, Comment, Like, Dislike, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id','post','topic')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author','body','post','created']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','author','post']

class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['id','author','post']

class PostSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    comments = CommentSerializer(many=True, read_only=True, required=False)
    likes = LikeSerializer(many=True, read_only=True, required=False)
    dislikes = DislikeSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Post
        fields = ('id','author','body','timestamp','livestatus','topics','comments','likes','dislikes')

    def create(self, validated_data):
        topics = validated_data.pop('topics')
        post = Post.objects.create(**validated_data)

        for topic in topics:
            print(topic)
            Topic.objects.create(
                    post=post,
                    **topic
                    )
        print('returned:',post.topics)
        return post
