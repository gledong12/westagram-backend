from django.db   import models
from user.models import User

class Post(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url  = models.URLField(max_length=10000)

    class Meta:
        db_table = 'posts'
