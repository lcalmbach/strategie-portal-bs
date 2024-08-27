# Generated by Django 5.0.7 on 2024-08-27 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "objective_manager_app",
            "0008_rename_bemerkungen_code_mv_planrecord_rueckmeldung_code_mv_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="planrecord",
            name="fortschritt",
        ),
        migrations.AlterField(
            model_name="organisation",
            name="bereich",
            field=models.CharField(max_length=200, verbose_name="Bereich"),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="bereich_kuerzel",
            field=models.CharField(max_length=200, verbose_name="Bereich Kürzel"),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="departement",
            field=models.CharField(max_length=200, verbose_name="Departement"),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="departement_kuerzel",
            field=models.CharField(max_length=200, verbose_name="Departement Kürzel"),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="dienststelle",
            field=models.CharField(max_length=200, verbose_name="Dienststelle"),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="dienststelle_kuerzel",
            field=models.CharField(max_length=200, verbose_name="Dienststelle Kürzel"),
        ),
        migrations.AlterField(
            model_name="person",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="objective_manager_app.organisation",
                verbose_name="Organisation",
            ),
        ),
        migrations.AlterField(
            model_name="planrecord",
            name="rueckmeldung_code_mv",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="planrecord_bemerkungen_code_mv",
                to="objective_manager_app.rueckmeldungmv",
                verbose_name="Probleme bei der Umsetzung der Massnahme",
            ),
        ),
        migrations.AlterField(
            model_name="planrecord",
            name="rueckmeldung_mv",
            field=models.TextField(
                blank=True, null=True, verbose_name="Allgmeine Bemerkungen"
            ),
        ),
        migrations.AlterField(
            model_name="planrecord",
            name="umsetzung_mv",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Welche Schritte, Teilprojekte oder Meilensteine wurden im Berichtsjahr umgesetzt?",
            ),
        ),
        migrations.AlterField(
            model_name="planrecord",
            name="zufriedenheit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="planrecord_zufriedenheit",
                to="objective_manager_app.wertung",
                verbose_name="Wie zufrieden sind Sie mit der Umsetzung der Massnahme",
            ),
        ),
    ]
