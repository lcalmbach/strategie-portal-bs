# Generated by Django 5.0.7 on 2024-08-03 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0018_alter_person_options_strategiedokument'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planrecord',
            name='objekt',
        ),
        migrations.AddField(
            model_name='planrecord',
            name='massnahme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='objective_manager_app.massnahmeorganisation', verbose_name='Massnahme'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='strategiedokument',
            name='strategie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dokumente', to='objective_manager_app.strategie'),
        ),
    ]
