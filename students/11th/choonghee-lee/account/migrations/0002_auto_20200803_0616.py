# Generated by Django 3.0.3 on 2020-08-03 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=40),
        ),
    ]