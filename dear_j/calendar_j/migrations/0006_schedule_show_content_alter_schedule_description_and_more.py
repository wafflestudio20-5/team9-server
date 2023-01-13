# Generated by Django 4.1.1 on 2023-01-13 21:39

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("calendar_j", "0005_alter_schedule_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedule",
            name="show_content",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="protection_level",
            field=models.IntegerField(choices=[(1, "Open"), (2, "Follower"), (3, "Closed")], default=1),
        ),
    ]
