# Generated by Django 3.0.8 on 2020-08-12 13:07

import User.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20200805_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=156, validators=[User.validators.validate_password]),
        ),
    ]
