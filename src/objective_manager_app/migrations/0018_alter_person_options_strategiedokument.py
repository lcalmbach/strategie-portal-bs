# Generated by Django 5.0.7 on 2024-08-03 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objective_manager_app', '0017_massnahmeorganisation_person'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['nachname', 'vorname']},
        ),
        migrations.CreateModel(
            name='StrategieDokument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel_dokument', models.TextField(max_length=200, verbose_name='Titel Dokument')),
                ('url_feld', models.URLField(max_length=500, verbose_name='Webseite')),
                ('strategie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='objective_manager_app.strategie')),
            ],
        ),
    ]
