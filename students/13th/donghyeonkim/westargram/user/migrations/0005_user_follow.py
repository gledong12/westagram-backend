# Generated by Django 3.1.1 on 2020-10-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20201009_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(related_name='follows', to='user.User'),
        ),
    ]