# Generated by Django 5.0.7 on 2024-08-05 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0025_planrecord_bedarf_unterstuetzung_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='massnahmeorganisation',
            name='bemerkungen',
            field=models.TextField(blank=True, null=True, verbose_name='Bemerkungen'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='bedarf_unterstuetzung',
            field=models.TextField(blank=True, help_text='Benötigest du Beratung oder Unterstützung zur Umsetzung der Massnahme?', null=True, verbose_name='Unterstützung'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='ergebnisse',
            field=models.TextField(blank=True, help_text='Liste der umgesetzten Elemente für diese Massnahme und deren Erfolge', null=True, verbose_name='Ergebnisse/Erfolge'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='schwierigkeiten',
            field=models.TextField(blank=True, help_text='Beschreibung der Schwierigkeiten bei der Umsetzung der Massnahme', null=True, verbose_name='Schwierigkeiten'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='schwierigkeiten_note',
            field=models.TextField(blank=True, help_text='Einstufung der Schwierigkeiten bei der Umsetzung von 1 (keine) bis 5 (sehr grosse)', null=True, verbose_name='Schwierigkeiten (1-5)'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='zufriedenheit_note',
            field=models.IntegerField(blank=True, help_text='Einstufung der Zufriedenheit mit der Umsetzung der Massnahme von 1 (sehr unzufrieden) bis 5 (sehr zufrieden)', null=True, verbose_name='Zufriedenheit (1-5)'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='zufriedenheit_text',
            field=models.TextField(blank=True, help_text='Zufriedenheit mit der Umsetzung der Massnahme', null=True, verbose_name='Zufriedenheit'),
        ),
    ]
