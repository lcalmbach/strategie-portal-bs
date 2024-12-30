# Generated by Django 5.0.7 on 2024-07-23 05:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "objective_manager_app",
            "0006_organisation_person_remove_planrecord_organisation_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="org",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="objective_manager_app.organisation",
            ),
            preserve_default=False,
        ),
    ]
