from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
#from taggit.managers import TaggableManager
from django.urls import reverse

class Post(models.Model):
    title = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now())
    body = models.TextField()
    title = models.CharField(max_length=250)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')

    def __str__(self):
        return self.body[:100]

    def get_url(self):
        return reverse('piazza:post',args=[self.id])

    def get_id(self):
        return self.id

    @property
    def expiration(self):
        return self.timestamp + timedelta(minutes=20)

    @property
    def islive(self):

        now = timezone.now()
        print(now,self.expiration)
        if now > self.expiration:
            return False
        else: return True

    @property
    def author(self):
        return User.objects.get(id=self.author_id.id).username

    class Meta:
        ordering = ('-timestamp',)




class Topic(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='topics', null=True, blank=True)
    topic = models.CharField(max_length=250)


"""
class Topic(models.Model):
    TOPICS = (
        ('Politics','politics'),
        ('Health','health'),
        ('Sport','sport'),
        ('Tech','tech'),
    )
    topic = models.CharField(max_length=10,choices=TOPICS)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="topic")
    def __str__(self):
        return self.topic
"""

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="likes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_author')

    class Meta:
        ordering = ('post',)

    def __str__(self):
        return f'Author {self.author}, Post {self.post}'

class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="dislikes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes_author')

    class Meta:
        ordering = ('post',)

    def __str__(self):
        return f'Author {self.author}, Post {self.post}'
