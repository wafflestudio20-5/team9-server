# Generated by Django 4.1.1 on 2023-01-28 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0009_user_birthday_user_birthyear"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(null=True, upload_to="user"),
        ),
    ]
