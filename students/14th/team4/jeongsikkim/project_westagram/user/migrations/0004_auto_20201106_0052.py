# Generated by Django 3.1.3 on 2020-11-06 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20201105_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='signup',
            name='login_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='signup',
            name='mobile_number',
            field=models.CharField(max_length=13),
        ),
    ]
