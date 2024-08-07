# Generated by Django 3.2.20 on 2024-07-17 08:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocklist', '0005_auto_20240717_0709'),
    ]

    operations = [
        migrations.CreateModel(
            name='Threshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name_plural': 'Thresholds',
            },
        ),
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.RemoveIndex(
            model_name='item',
            name='stocklist_i_name_e52989_idx',
        ),
        migrations.AddField(
            model_name='threshold',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='threshold', to='stocklist.item'),
        ),
    ]
