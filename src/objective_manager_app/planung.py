from datetime import date
import calendar
from .models import MassnahmeOrganisation, PlanRecord


class Planung:
    def __init__(self, user):
        self.user = user
        self.jahr

    def run(self):
        organisation_massnahmen = MassnahmeOrganisation.objects.filter(
            jahr=self.jahr
        )
        # bestehende Planrecords löschen
        PlanRecord.objects.filter(
            jahr=self.jahr
        ).delete()

        for organisation_massnahme in organisation_massnahmen:
            massnahme = organisation_massnahme.massnahme
            last_day_of_december = date(self.jahr, 12, calendar.monthrange(self.jahr, 12)[1])

            PlanRecord.objects.create(
                massnahme=massnahme,
                verantwortlich=organisation_massnahme,
                jahr=self.jahr,
                monat=12,
                faellig_am=last_day_of_december,
                erstellt_von=self.user
            )


