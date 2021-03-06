from django.db   import models

from user.models import User

class Post(models.Model):
    user        = models.ForeignKey('user.User', on_delete=models.CASCADE) 
    image_url   = models.URLField(max_length=500)
    content     = models.TextField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    liked_users = models.ManyToManyField('user.User', through='Like', related_name='liked_posts')

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post       = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent     = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    content    = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
