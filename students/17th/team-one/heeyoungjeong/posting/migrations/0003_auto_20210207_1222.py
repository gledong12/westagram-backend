# Generated by Django 3.1.5 on 2021-02-07 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0002_auto_20210207_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='posting',
            name='modify_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
