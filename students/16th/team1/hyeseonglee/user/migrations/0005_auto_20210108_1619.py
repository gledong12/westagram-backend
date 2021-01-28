# Generated by Django 3.1.5 on 2021-01-08 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210108_1616'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ('-created_dt',), 'verbose_name': 'follow', 'verbose_name_plural': 'follows'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('email',), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='follow_time',
            new_name='created_dt',
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(db_column='follower', on_delete=django.db.models.deletion.CASCADE, related_name='who_is_followed', to='user.user'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(db_column='following', on_delete=django.db.models.deletion.CASCADE, related_name='who_follows', to='user.user'),
        ),
    ]
