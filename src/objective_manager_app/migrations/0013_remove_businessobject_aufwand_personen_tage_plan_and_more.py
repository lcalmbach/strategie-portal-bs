# Generated by Django 5.0.7 on 2024-08-27 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0012_alter_planrecord_rueckmeldung_anderes_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessobject',
            name='aufwand_personen_tage_plan',
        ),
        migrations.RemoveField(
            model_name='businessobject',
            name='aufwand_tsd_chf_plan',
        ),
        migrations.RemoveField(
            model_name='businessobject',
            name='jahr_start',
        ),
        migrations.RemoveField(
            model_name='planrecord',
            name='faellig_am',
        ),
        migrations.AlterField(
            model_name='businessobject',
            name='jahr_ende',
            field=models.IntegerField(default=2024, verbose_name='Termin'),
        ),
    ]
