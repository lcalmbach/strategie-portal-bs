from datetime import date
import calendar
from .models import MassnahmeOrganisation, PlanRecord


class Planung:
    def __init__(self, strategie, user):
        self.strategie = strategie
        self.user = user

    def run(self):
        organisation_massnahmen = MassnahmeOrganisation.objects.filter(
            massnahme__strategie=self.strategie
        )
        # bestehende Planrecords löschen
        PlanRecord.objects.filter(strategie=self.strategie).delete()
        for organisation_massnahme in organisation_massnahmen:
            for year in range(
                organisation_massnahme.massnahme.jahr_start,
                organisation_massnahme.massnahme.jahr_ende + 1,
            ):
                massnahme = organisation_massnahme.massnahme
                last_day_of_december = date(year, 12, calendar.monthrange(year, 12)[1])
                num_years = massnahme.jahr_ende - massnahme.jahr_start + 1
                fortschritt_pzt_plan = 100 / num_years
                aufwand_personen_tage_plan = (
                    massnahme.aufwand_personen_tage_plan / num_years
                    if massnahme.aufwand_personen_tage_plan > 0
                    else 0
                )
                aufwand_tsd_chf_plan = (
                    massnahme.aufwand_tsd_chf_plan / num_years
                    if massnahme.aufwand_tsd_chf_plan > 0
                    else 0
                )

                PlanRecord.objects.create(
                    strategie=self.strategie,
                    verantwortlich=organisation_massnahme,
                    jahr=year,
                    monat=12,
                    faellig_am=last_day_of_december,
                    fortschritt_pzt_plan=fortschritt_pzt_plan,
                    aufwand_personen_tage_plan=aufwand_personen_tage_plan,
                    aufwand_tsd_chf_plan=aufwand_tsd_chf_plan,
                    erstellt_von=self.user,
                )
