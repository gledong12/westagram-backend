# Generated by Django 3.1.4 on 2021-01-09 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0009_auto_20210109_1911'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='reply',
            new_name='comment',
        ),
    ]
