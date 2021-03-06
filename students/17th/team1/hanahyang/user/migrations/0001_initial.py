# Generated by Django 3.1.5 on 2021-01-31 05:46

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
                ('email', models.EmailField(max_length=50, null=True, unique=True)),
                ('name', models.CharField(max_length=20, null=True, unique=True)),
                ('phone', models.CharField(max_length=15, null=True, unique=True)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
