# Generated by Django 3.1.5 on 2021-02-03 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210202_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_adress',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=50),
        ),
    ]
