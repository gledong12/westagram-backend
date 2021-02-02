# Generated by Django 3.1.4 on 2021-01-01 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.BinaryField(max_length=500)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
