# Generated by Django 5.0.7 on 2024-08-23 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0003_planrecord_massnahme_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planrecord',
            old_name='Massnahme',
            new_name='massnahme',
        ),
    ]