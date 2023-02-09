# Generated by Django 4.1.5 on 2023-02-09 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minted', '0017_remove_spendinglimit_limit_spendinglimit_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spendinglimit',
            name='timeframe',
            field=models.CharField(blank=True, choices=[('/week', 'week'), ('/month', 'month'), ('/quarter', 'quarter'), ('/year', 'year')], max_length=11),
        ),
    ]