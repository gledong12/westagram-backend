# Generated by Django 3.1.5 on 2021-02-04 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0002_auto_20210204_1857'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='postlike',
            table='postlikes',
        ),
    ]