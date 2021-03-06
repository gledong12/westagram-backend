# Generated by Django 3.1.6 on 2021-02-02 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('phonenumber', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
    ]
