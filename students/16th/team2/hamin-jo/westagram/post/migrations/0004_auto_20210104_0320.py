# Generated by Django 3.1.4 on 2021-01-04 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('post', '0003_model'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Model',
            new_name='Comment',
        ),
    ]