# Generated by Django 3.1.5 on 2021-02-05 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='posting',
            new_name='post',
        ),
    ]