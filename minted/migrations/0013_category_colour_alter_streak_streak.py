# Generated by Django 4.1.5 on 2023-03-10 15:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minted', '0012_alter_points_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='colour',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='streak',
            name='streak',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
