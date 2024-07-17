# Generated by Django 3.2.20 on 2024-07-17 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocklist', '0004_auto_20240717_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='reorder_level',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]