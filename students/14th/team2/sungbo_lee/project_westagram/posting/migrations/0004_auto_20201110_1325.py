# Generated by Django 3.1.3 on 2020-11-10 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0003_auto_20201110_1222'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='comment',
            table='comments',
        ),
    ]
