# Generated by Django 3.1.3 on 2020-11-07 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20201106_0716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_id',
            new_name='user_name',
        ),
    ]