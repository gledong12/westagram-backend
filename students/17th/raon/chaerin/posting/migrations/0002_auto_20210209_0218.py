# Generated by Django 3.1.5 on 2021-02-09 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='image_url',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
