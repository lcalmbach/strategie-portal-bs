# Generated by Django 5.0.7 on 2024-12-23 10:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "objective_manager_app",
            "0040_rename_faellig_am_planrecord_ende_datum_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="businessobjectthema",
            name="ebene",
        ),
        migrations.AddField(
            model_name="thema",
            name="ebene",
            field=models.IntegerField(default=1, verbose_name="Ebene"),
        ),
        migrations.AlterField(
            model_name="businessobjectthema",
            name="business_object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="themen_business_objects",
                to="objective_manager_app.businessobject",
            ),
        ),
        migrations.AlterField(
            model_name="businessobjectthema",
            name="thema",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="business_objects_themen",
                to="objective_manager_app.thema",
            ),
        ),
    ]
