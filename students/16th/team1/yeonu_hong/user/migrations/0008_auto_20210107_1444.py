# Generated by Django 3.1.4 on 2021-01-07 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20210106_0514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=130, null=True),
        ),
    ]
