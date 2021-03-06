from django.db   import models

from user.models import User

class Post(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url  = models.URLField(max_length=1000)
    like       = models.IntegerField(default=0)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    post           = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    user           = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now_add=True)
    comment_body   = models.TextField(max_length=10000)

    class Meta:
        db_table = 'comments'

class PostLike(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        db_table = 'postlikes'

class Follow(models.Model):
    from_user = models.ForeignKey('user.User', related_name="from_users", on_delete=models.CASCADE)
    to_user   = models.ForeignKey('user.User', related_name="to_users", on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'follows'