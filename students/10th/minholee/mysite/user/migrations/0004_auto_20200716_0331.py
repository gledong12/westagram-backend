# Generated by Django 3.0.8 on 2020-07-16 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200715_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=511),
        ),
    ]
