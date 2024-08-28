# Generated by Django 5.0.7 on 2024-08-27 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0013_remove_businessobject_aufwand_personen_tage_plan_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JaNein',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('objective_manager_app.code',),
        ),
        migrations.CreateModel(
            name='Zufriedenheit',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('objective_manager_app.code',),
        ),
        migrations.AddField(
            model_name='planrecord',
            name='einhaltung_termin_text',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Begründung der Abweichung'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='einhaltung_termin',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planrecord_einhaltung_termin', to='objective_manager_app.janein', verbose_name='Termin wird eingehalten'),
        ),
        migrations.AlterField(
            model_name='planrecord',
            name='zufriedenheit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planrecord_zufriedenheit', to='objective_manager_app.zufriedenheit', verbose_name='Wie zufrieden sind Sie mit der Umsetzung der Massnahme'),
        ),
    ]
