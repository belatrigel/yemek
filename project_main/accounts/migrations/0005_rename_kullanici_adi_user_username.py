# Generated by Django 4.2.7 on 2023-11-26 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='kullanici_adi',
            new_name='username',
        ),
    ]
