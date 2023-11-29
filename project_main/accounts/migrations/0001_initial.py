# Generated by Django 4.2.7 on 2023-11-25 20:36

import accounts.models
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('joined_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'işletmeci'), (2, 'müşteri')], null=True)),
                ('isim', models.CharField(max_length=255, verbose_name='Adınız')),
                ('soyisim', models.CharField(max_length=255, verbose_name='Soyisminiz')),
                ('kullanici_adi', models.CharField(max_length=64, unique=True, verbose_name='Takma isminiz')),
                ('elmek', models.EmailField(max_length=128, unique=True)),
                ('phone', models.CharField(max_length=13, validators=[accounts.models.validate_phone_format])),
                ('password', models.CharField(max_length=128, verbose_name='sifre')),
                ('is_yonetici', models.BooleanField(default=False)),
                ('is_aktif', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_ustyonetici', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('yonetici', django.db.models.manager.Manager()),
            ],
        ),
    ]
