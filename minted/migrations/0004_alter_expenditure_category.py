# Generated by Django 4.1.5 on 2023-01-31 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minted', '0003_expenditure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenditure',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minted.category'),
        ),
    ]
