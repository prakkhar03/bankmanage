# Generated by Django 5.0.6 on 2024-07-01 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('aadhar_number', models.CharField(max_length=12, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('date_of_birth', models.DateField()),
                ('address', models.TextField()),
                ('password', models.CharField(max_length=128)),
                ('balance', models.FloatField()),
            ],
        ),
    ]
