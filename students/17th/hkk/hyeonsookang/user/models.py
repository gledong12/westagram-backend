from django.db import models

class User(models.Model):
    email       = models.CharField(max_length=30)
    phonenumber = models.IntegerField(default=0)
    account     = models.CharField(max_length=30)
    password    = models.CharField(max_length=30)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Users'
