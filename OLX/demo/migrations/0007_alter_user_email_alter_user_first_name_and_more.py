# Generated by Django 5.1.4 on 2024-12-26 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0006_user_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
