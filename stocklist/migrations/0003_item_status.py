# Generated by Django 3.2.20 on 2024-04-06 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocklist', '0002_auto_20240406_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
