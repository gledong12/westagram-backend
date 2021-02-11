from django.db import models

# Create your models here.
class User(models.Model):
    mobile      = models.CharField(max_length=200, null=True)
    email       = models.EmailField(max_length=200, unique=True)
    full_name   = models.CharField(max_length=45)
    username    = models.CharField(max_length=45, unique=True)
    password    = models.CharField(max_length=300)
    follow      = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return self.username
    
    class Meta():
        db_table = 'users'
