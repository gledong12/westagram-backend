# Generated by Django 3.1.2 on 2020-10-12 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20201009_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(to='user.User'),
        ),
    ]
