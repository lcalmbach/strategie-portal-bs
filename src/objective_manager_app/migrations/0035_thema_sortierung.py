# Generated by Django 5.0.7 on 2024-12-23 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("objective_manager_app", "0034_thema_kuerzel_alter_thema_wunschrichtung"),
    ]

    operations = [
        migrations.AddField(
            model_name="thema",
            name="sortierung",
            field=models.IntegerField(default=0),
        ),
    ]
