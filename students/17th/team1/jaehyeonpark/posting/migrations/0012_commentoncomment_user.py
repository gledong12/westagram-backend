# Generated by Django 3.1.5 on 2021-02-05 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_follow'),
        ('posting', '0011_commentoncomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentoncomment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
            preserve_default=False,
        ),
    ]
