# Generated by Django 3.1.5 on 2021-02-12 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0008_auto_20210209_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posting.comment'),
        ),
    ]
