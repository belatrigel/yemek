# Generated by Django 4.2.7 on 2024-01-14 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'katogori', 'verbose_name_plural': 'kategoriler'},
        ),
    ]