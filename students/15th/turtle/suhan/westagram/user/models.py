from django.db import models

# Create your models here.


class User(models.Model):
    email      = models.EmailField(max_length=100)
    password   = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
