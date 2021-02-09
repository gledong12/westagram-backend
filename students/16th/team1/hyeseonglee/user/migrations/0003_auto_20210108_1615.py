# Generated by Django 3.1.5 on 2021-01-08 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210106_0513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_time', models.DateTimeField(auto_now=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_is_followed', to='user.user')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_follows', to='user.user')),
            ],
            options={
                'verbose_name': 'follow',
                'verbose_name_plural': 'user',
                'db_table': 'follows',
                'ordering': ('-follow_time',),
            },
        ),
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(through='user.Follow', to='user.User'),
        ),
    ]