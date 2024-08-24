import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from objective_manager_app.models import MassnahmeOrganisation, PlanRecord, Person  # Adjust the import according to your actual app and model names
import random
import string
from datetime import date, datetime
import calendar



class Command(BaseCommand):
    help = 'Create a user for each person in the Person table'

    def handle(self, *args, **kwargs):
        year = 2024
        organisation_massnahmen = MassnahmeOrganisation.objects.all()
        # bestehende Planrecords löschen
        PlanRecord.objects.filter(
            jahr=year
        ).delete()

        for organisation_massnahme in organisation_massnahmen:
            massnahme = organisation_massnahme.massnahme
            last_day_of_december = date(year, 12, calendar.monthrange(year, 12)[1])

            PlanRecord.objects.create(
                massnahme=massnahme,
                verantwortlich=organisation_massnahme.person,
                organisation = organisation_massnahme.organisation,
                jahr=year,
                erstellt_am = datetime.now(),
                erstellt_von = User.objects.get(username='lcalm')
            )