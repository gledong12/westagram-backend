from django.db   import models

class Account(models.Model):
    email     = models.EmailField()
    name      = models.CharField(max_length=20)
    nickname  = models.CharField(max_length=30)
    password  = models.CharField(max_length=128)
    phone     = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __Str__(self):
        return f'{self.name} : {self:email}'
    class Meta:
        db_table = 'accounts'
