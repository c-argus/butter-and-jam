# Generated by Django 3.2.20 on 2024-08-01 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocklist', '0009_item_added_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
    ]
