# Generated by Django 4.1.1 on 2022-12-31 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_user_username"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="birthday",
            new_name="birthdate",
        ),
    ]
