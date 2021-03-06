# Generated by Django 3.1.5 on 2021-02-01 10:27

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='nicname',
            new_name='nickname',
        ),
        migrations.AddField(
            model_name='account',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31),
        ),
    ]
