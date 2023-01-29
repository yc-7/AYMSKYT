# Generated by Django 4.1.5 on 2023-01-29 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PST', '0005_alter_spendinglimit_timeframe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spendinglimit',
            name='timeframe',
            field=models.CharField(choices=[('/week', 'Weekly'), ('/month', 'Monthly'), ('/6 months', 'Half-yearly'), ('/year', 'Annually'), ('overall', 'Overall')], max_length=11),
        ),
    ]
