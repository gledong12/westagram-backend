from django.db import models

class Post(models.Model):

    title       = models.CharField(max_length=100)
    writer      = models.ForeignKey('users.User',related_name='posts', on_delete=models.CASCADE)
    content     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    # like        = models.ManyToManyField("users.User", related_name="posts", blank=True)

    class Meta:
        db_table = "posts"

class PostImage(models.Model):

    post    = models.ForeignKey('posts.Post', related_name="post_images", on_delete=models.CASCADE)
    img_url = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = "post_images"


class Comment(models.Model):
    
    post       = models.ForeignKey('posts.Post', related_name="comments", on_delete=models.CASCADE)
    user       = models.ForeignKey('users.User', related_name="comments", on_delete=models.CASCADE)
    recomment  = models.ForeignKey('Comment', related_name="comments", on_delete=models.CASCADE, null=True)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"

class Like(models.Model):

    user = models.ForeignKey("users.User", related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", related_name="likes", on_delete=models.CASCADE)

    class Meta:
        db_table = "likes"
