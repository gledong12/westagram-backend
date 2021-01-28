from django.db import models

class User(models.Model):
    name        = models.CharField(max_length  = 20)
    email       = models.EmailField(max_length = 100)
    password    = models.CharField(max_length  = 100)
    nickname    = models.CharField(max_length  = 150)
    phonenumber = models.CharField(max_length  = 15)

    class Meta:
        db_table = "users"

class Follow(models.Model):
    followee  = models.ForeignKey('User',on_delete=models.CASCADE, related_name='followee')
    follower  = models.ForeignKey('User',on_delete=models.CASCADE, related_name='follower')

    class Meta: db_table = "follows"