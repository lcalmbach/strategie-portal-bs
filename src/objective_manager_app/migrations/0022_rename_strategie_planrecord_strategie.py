# Generated by Django 5.0.7 on 2024-08-04 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0021_rename_massnahme_planrecord_verantwortlich_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planrecord',
            old_name='Strategie',
            new_name='strategie',
        ),
    ]
