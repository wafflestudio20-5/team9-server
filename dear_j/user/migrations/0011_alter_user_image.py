# Generated by Django 4.1.1 on 2023-01-29 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0010_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(
                blank=True, default="user/user.png", upload_to="user"
            ),
        ),
    ]
