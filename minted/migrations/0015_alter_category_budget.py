# Generated by Django 4.1.5 on 2023-02-09 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minted', '0014_alter_user_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='budget',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minted.spendinglimit'),
        ),
    ]