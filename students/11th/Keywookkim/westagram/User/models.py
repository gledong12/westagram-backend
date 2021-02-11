from django.db                       import models
from django.conf                     import settings
from django.db.models.signals        import post_save

from .validators                     import validate_email, validate_password

class User(models.Model):
    email        = models.EmailField(max_length = 50, validators = [validate_email])
    password     = models.CharField(max_length = 500, validators = [validate_password], null=False)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'accounts'

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)
