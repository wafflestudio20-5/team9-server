# Generated by Django 4.1.1 on 2023-01-17 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0006_rename_date_joined_user_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="birthdate",
            field=models.DateField(null=True),
        ),
    ]
