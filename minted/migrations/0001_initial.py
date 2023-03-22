# Generated by Django 4.1.5 on 2023-03-22 17:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('points', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('colour', models.CharField(blank=True, max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('points_required', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('reward_id', models.CharField(max_length=6, unique=True)),
                ('expiry_date', models.DateField()),
                ('description', models.TextField(max_length=300)),
                ('cover_image', models.FileField(blank=True, upload_to='rewards/')),
                ('code_type', models.CharField(choices=[('qr', 'QR Code'), ('random', 'Randomly Generated Code')], default='random', max_length=6)),
                ('user_limit', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='SpendingLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.DecimalField(decimal_places=2, max_digits=12)),
                ('timeframe', models.CharField(choices=[('/week', 'week'), ('/month', 'month'), ('/quarter', 'quarter'), ('/year', 'year')], max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Streak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login_time', models.DateTimeField(auto_now=True, null=True)),
                ('streak', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RewardClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('claim_qr', models.FileField(blank=True, upload_to='rewards/')),
                ('reward_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minted.reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.IntegerField(blank=True, choices=[(1, 'Daily'), (7, 'Weekly'), (30, 'Monthly')], null=True)),
                ('subscriptions', models.ManyToManyField(blank=True, to='minted.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=200)),
                ('receipt', models.FileField(blank=True, upload_to='uploads/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='minted.category')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='budget',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='minted.spendinglimit'),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='budget',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minted.spendinglimit'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='notification_subscription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='minted.notificationsubscription'),
        ),
        migrations.AddField(
            model_name='user',
            name='streak_data',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='minted.streak'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('user', 'name')},
        ),
    ]
