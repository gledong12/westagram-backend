# Generated by Django 3.1.5 on 2021-02-03 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
