# Generated by Django 4.1.1 on 2023-05-03 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfomodel',
            name='gender',
            field=models.CharField(choices=[('Select your gender', 'None'), ('Male', 'MALE'), ('Female', 'FEMALE'), ('Others', 'OTHERS')], max_length=18, verbose_name='Your gender'),
        ),
    ]
