from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
#from taggit.managers import TaggableManager
from django.urls import reverse
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_islive(post):
    if not post.islive:
        raise ValidationError(_('Post is expired'))

class Post(models.Model):
    title = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now())
    body = models.TextField()
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

    def save(self, *args, **kwargs):
        self.topic = self.topic.lower()
        return super(Topic, self).save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments", validators = [validate_islive])
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    @property
    def author(self):
        return User.objects.get(id=self.author_id.id).username

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Like(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="likes", validators = [validate_islive])
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_author')

    @property
    def author(self):
        return User.objects.get(id=self.author_id.id).username

    class Meta:
        ordering = ('post',)

    def __str__(self):
        return f'Author {self.author}, Post {self.post}'

class Dislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="dislikes")
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes_author')

    @property
    def author(self):
        return User.objects.get(id=self.author_id.id).username

    class Meta:
        ordering = ('post',)

    def __str__(self):
        return f'Author {self.author}, Post {self.post}'
