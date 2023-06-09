# Generated by Django 4.1.1 on 2023-05-31 16:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(null=True, verbose_name='Your Date of Birth')),
                ('gender', models.CharField(choices=[('None', 'Select your gender'), ('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHERS', 'Others')], max_length=18, verbose_name='Your gender')),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message='Please enter your country code and your phone number.', regex='^\\+?1?\\d{9,15}$')], verbose_name='Your Phone Number')),
                ('address', models.CharField(max_length=300, verbose_name='Your address')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Your country')),
                ('state', models.CharField(max_length=50, verbose_name='Your State')),
                ('city', models.CharField(max_length=50, verbose_name='Your City')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
