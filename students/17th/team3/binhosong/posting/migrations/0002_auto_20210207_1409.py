# Generated by Django 3.1.5 on 2021-02-07 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210204_0759'),
        ('posting', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='post',
            table='postings',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.account')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.post')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
    ]
