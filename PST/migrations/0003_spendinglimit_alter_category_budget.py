# Generated by Django 4.1.5 on 2023-01-29 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PST', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpendingLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.DecimalField(decimal_places=2, default=None, max_digits=12)),
                ('time', models.CharField(choices=[('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('HALF-YEARLY', 'Half-yearly'), ('ANNUALLY', 'Annually'), ('OVERALL', 'Overall')], max_length=11)),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='budget',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='PST.spendinglimit'),
        ),
    ]
