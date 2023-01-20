# Generated by Django 4.1.1 on 2023-01-18 01:19
from django.apps import registry
from django.contrib.sites import models
from django.db import migrations

from dear_j import settings


def setup_default_site(apps: registry.Apps, schema_editor):
    """
    Set up or rename the default example.com site created by Django.
    """
    Site = apps.get_model("sites", "Site")

    site, _ = Site.objects.get_or_create(pk=settings.SITE_ID)
    site.name = settings.NAME
    site.domain = settings.DOMAIN
    site.save()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0007_alter_user_birthdate"),
    ]

    operations = [
        migrations.RunPython(setup_default_site, migrations.RunPython.noop),
    ]
