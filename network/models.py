from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    liked_posts = models.ManyToManyField('Post', symmetrical=False, related_name='liked', blank=True)
    liked_comments = models.ManyToManyField('Comment', symmetrical=False, related_name='liked_comment', blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    biography = models.TextField(max_length=300, blank=True)

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1200,blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.TextField(blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    comment = models.TextField(max_length=300, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class PostEngagement(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='engagement')
    page_rank = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    engagement_time = models.IntegerField(default=0)

class CommentEngagement(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='engagement')
    comment_rank = models.DecimalField(max_digits=5, decimal_places=2, default=0)