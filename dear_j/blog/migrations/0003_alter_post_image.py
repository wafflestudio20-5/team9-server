# Generated by Django 4.1.1 on 2023-01-28 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(null=True, upload_to="post"),
        ),
    ]
