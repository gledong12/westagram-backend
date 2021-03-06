# Generated by Django 3.1.5 on 2021-02-08 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210204_0409'),
        ('posting', '0004_auto_20210207_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now=True)),
                ('posting', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posting.posting')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user')),
            ],
            options={
                'db_table': 'Comment',
            },
        ),
    ]
