# Generated by Django 5.0.7 on 2024-12-30 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "objective_manager_app",
            "0002_remove_businessobject_anmerkung_initialisierung",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="businessobject",
            name="mess_groesse",
        ),
    ]
