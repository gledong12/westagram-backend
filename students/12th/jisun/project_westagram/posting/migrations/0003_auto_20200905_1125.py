# Generated by Django 3.1 on 2020-09-05 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200901_1426'),
        ('posting', '0002_auto_20200903_0906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posting',
            old_name='writer',
            new_name='user',
        ),
        migrations.CreateModel(
            name='Commenting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment_contents', models.CharField(max_length=100)),
                ('image_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.posting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.users')),
            ],
            options={
                'db_table': 'commenting',
            },
        ),
    ]
