# Generated by Django 4.2.11 on 2024-04-24 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RentHubAPI', '0002_remove_listing_property_type_listing_property_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='listing',
        ),
    ]