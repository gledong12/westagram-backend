# Generated by Django 3.1.5 on 2021-02-10 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210209_1720'),
        ('posting', '0010_auto_20210208_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='depth',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='posting.comment'),
        ),
        migrations.AlterField(
            model_name='userpostinglike',
            name='posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.posting'),
        ),
        migrations.AlterField(
            model_name='userpostinglike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]
