# Generated by Django 3.1.5 on 2021-02-01 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('Phone_number', models.IntegerField(unique=True)),
                ('email', models.CharField(max_length=25, unique=True)),
                ('password', models.CharField(default=0, max_length=25)),
            ],
            options={
                'db_table': 'userinfo',
            },
        ),
    ]
