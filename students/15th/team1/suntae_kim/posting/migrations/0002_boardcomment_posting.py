# Generated by Django 3.1.4 on 2020-12-06 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardcomment',
            name='posting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posting.boardposting'),
        ),
    ]