# Generated by Django 3.1.4 on 2021-01-06 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0003_post_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='img',
            new_name='image_url',
        ),
        migrations.AlterModelTable(
            name='post',
            table='posts',
        ),
    ]
