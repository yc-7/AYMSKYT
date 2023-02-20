# Generated by Django 4.1.5 on 2023-02-20 13:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minted', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='budget',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
