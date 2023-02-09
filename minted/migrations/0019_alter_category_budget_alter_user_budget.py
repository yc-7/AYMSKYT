# Generated by Django 4.1.5 on 2023-02-09 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('minted', '0018_alter_spendinglimit_timeframe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='budget',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='minted.spendinglimit'),
        ),
        migrations.AlterField(
            model_name='user',
            name='budget',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='minted.spendinglimit'),
        ),
    ]