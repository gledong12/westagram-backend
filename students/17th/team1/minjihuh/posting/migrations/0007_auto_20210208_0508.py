# Generated by Django 3.1.5 on 2021-02-08 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0006_like'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='like',
            table='likes',
        ),
    ]
