# Generated by Django 4.1.1 on 2023-05-19 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.CharField(max_length=200, verbose_name='Wallet ID')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('pending', models.BooleanField(default=True, verbose_name='Pending Transactions')),
                ('rejected', models.BooleanField(default=False, verbose_name='Rejected/Canceled Transactions')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Users_info')),
            ],
        ),
    ]
