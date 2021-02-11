from django.db import models

class User(models.Model):
    email      = models.EmailField(max_length=45, null=True)
    phone      = models.CharField(max_length=45, null=True)
    name       = models.CharField(max_length=45)
    user_name  = models.CharField(max_length=45)
    password   = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"email:{self.email}, phone:{self.phone}, name:{self.name}," \
               f"user_name:{self.user_name}, password:{self.password}"
    
    class Meta:
        db_table = 'users'

class Follow(models.Model):
    who      = models.ForeignKey('user.User',
                                 on_delete=models.CASCADE,
                                 blank    =True,
                                 null     =True)
    follower = models.IntegerField(null=True)
    followee = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'follows'