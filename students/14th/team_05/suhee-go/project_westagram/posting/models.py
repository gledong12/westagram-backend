from django.db import models

class Post(models.Model):
    author     = models.ForeignKey('user.User', on_delete = models.CASCADE)
    image_url  = models.URLField(max_length = 200)
    content    = models.TextField(verbose_name = "내용", blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'posts'


class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete = models.CASCADE)
    author     = models.ForeignKey('user.User', on_delete = models.CASCADE)
    content    = models.TextField(max_length = 240)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'comments'
