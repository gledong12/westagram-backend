# Generated by Django 3.1.5 on 2021-02-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210201_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
