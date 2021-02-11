from django.db import models

class User(models.Model):
    email      = models.EmailField(max_length = 30)
    password   = models.CharField(max_length = 30)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return self.email