# Generated by Django 3.1.4 on 2021-01-05 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210105_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
