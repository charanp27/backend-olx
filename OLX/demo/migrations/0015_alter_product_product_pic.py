# Generated by Django 5.1.4 on 2024-12-31 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0014_alter_product_product_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_pic',
            field=models.CharField(max_length=1000000),
        ),
    ]