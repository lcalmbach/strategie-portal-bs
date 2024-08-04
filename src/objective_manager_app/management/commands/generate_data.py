import random
from django.core.management.base import BaseCommand
from objective_manager_app.models import (
    MassnahmeOrganisation,
    CodeKategorie, 
    Code, 
    BusinessObject, 
    Person, 
    Organisation, 
    Ziel, 
    Massnahme, 
    BusinessObjectTyp, 
    NeuBestehend,
    Strategie
)
from django.contrib.auth.models import User
from faker import Faker
import pandas as pd
import os
from django.conf import settings
from django.db import transaction

class Command(BaseCommand):
    help = 'Generate fake data for the ziel_manager app'

    def handle(self, *args, **kwargs):
        faker = Faker('de_DE')

        def generate_personen():
            code_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'person.csv')
            person_df = pd.read_csv(code_filename, sep=';')
            for person in person_df.itertuples():
                Person.objects.create(
                    id=person.id,
                    vorname=person.vorname,
                    nachname=person.nachname,
                )
        
        def generate_organisationen():
            code_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'organisation.csv')
            organisation_df = pd.read_csv(code_filename, sep=';')
            with transaction.atomic():
                for organisation in organisation_df.itertuples():
                    organisation_defaults = {
                        'departement': organisation.departement,
                        'bereich': organisation.bereich,
                        'dienststelle': organisation.dienststelle,
                        'departement_kuerzel': organisation.departement_kuerzel,
                        'bereich_kuerzel': organisation.bereich_kuerzel,
                        'dienststelle_kuerzel': organisation.dienststelle_kuerzel
                    }

                    # Use get_or_create to handle checking and creating in one step
                    _, created = Organisation.objects.get_or_create(
                        id=organisation.id,
                        defaults=organisation_defaults
                    )

                    # Optional: log or print the action
                    if created:
                        print(f"Created new organisation with id {organisation.id}")
                    else:
                        print(f"Organisation with id {organisation.id} already exists")

        def generate_codes():
            code_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'code.csv')
            category_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'code_kategorie.csv')

            category_df = pd.read_csv(category_filename, sep=';')
            code_df = pd.read_csv(code_filename, sep=';')

            # Clear existing data
            CodeKategorie.objects.all().delete()
            Code.objects.all().delete()

            # Create CodeKategorie objects
            for cat in category_df.itertuples():
                CodeKategorie.objects.create(
                    id=cat.id, 
                    titel=cat.titel, 
                    beschreibung=cat.beschreibung
                )

            # Create Code objects
            for code in code_df.itertuples():
                print(code)
                Code.objects.create(
                    id=code.id,
                    kategorie=CodeKategorie.objects.get(id=code.kategorie_id),  # Correctly reference the foreign key
                    titel=code.titel,
                    beschreibung=code.beschreibung
                )
        
        def generate_themen():
            themen_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'themen.csv')
            themen_df = pd.read_csv(themen_filename, sep=';')
            for thema in themen_df.itertuples():
                BusinessObject.objects.create(
                    typ=Code.objects.get(id=1),
                    kuerzel=thema.kuerzel,
                    titel=thema.titel,
                    beschreibung=thema.beschreibung,
                    erstellt_von=User.objects.first()   
                )
            
        def generate_handlungsfelder():
            handlungsfelder_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'handlungsfelder.csv')
            handlungsfelder_df = pd.read_csv(handlungsfelder_filename, sep=';')
            for handlungsfeld in handlungsfelder_df.itertuples():
                BusinessObject.objects.create(
                    typ=Code.objects.get(id=2),
                    vorgaenger=BusinessObject.objects.get(kuerzel=handlungsfeld.thema),
                    titel=handlungsfeld.titel,
                    beschreibung=handlungsfeld.beschreibung,
                    erstellt_von=User.objects.first(),
                    kuerzel=handlungsfeld.kuerzel   
                )

        def generate_ziele():
            ziele_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'ziele.csv')
            ziele_df = pd.read_csv(ziele_filename, sep=';')
            for ziel in ziele_df.itertuples():
                BusinessObject.objects.create(
                    typ=Code.objects.get(id=3),
                    vorgaenger=BusinessObject.objects.get(kuerzel=ziel.handlungsfeld),
                    titel=ziel.titel,
                    beschreibung=ziel.beschreibung,
                    erstellt_von=User.objects.first(),
                    kuerzel=ziel.kuerzel      
                )
        
        
        def generate_massnahmen():
            Massnahme.objects.all().delete()
            massnahmen_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'massnahmen.csv')
            massnahmen_df = pd.read_csv(massnahmen_filename, sep=';')
            massnahmen_df.fillna(0, inplace=True)
            for massnahme in massnahmen_df.itertuples():
                BusinessObject.objects.create(
                    strategie = Strategie.objects.get(id=2),
                    typ=Code.objects.get(id=4),
                    vorgaenger=Ziel.objects.filter(kuerzel=massnahme.ziel, strategie_id=2).first(),
                    titel=massnahme.titel,
                    beschreibung=massnahme.titel,
                    erstellt_von=User.objects.first(),
                    kuerzel=massnahme.kuerzel,
                    anmerkung_initialisierung=massnahme.anmerkung,
                    jahr_start=massnahme.jahr_start,
                    jahr_ende=massnahme.jahr_ende,
                    bestehende_massnahme=NeuBestehend.objects.get(id=6) if massnahme.bestehend_neu == 'bestehend' else NeuBestehend.objects.get(id=5),
                    aufwand_personen_tage_plan=massnahme.hc if massnahme.hc is not None else 0,
                    aufwand_tsd_chf_plan=massnahme.kosten if massnahme.kosten is not None else 0,

                )
        
        def generate_org_massnahme_beziehung():
            filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'org_massnahme.csv')
            org_massn_df = pd.read_csv(filename, sep=';')
            with transaction.atomic():
                for record in org_massn_df.itertuples():
                    try:
                        # Ensure all required fields are valid
                        if all([record.kuerzel_massnahme, record.pers_id, record.org_id]):
                            massnahme = Massnahme.objects.filter(kuerzel=record.kuerzel_massnahme, strategie_id=2).first()
                            organisation = Organisation.objects.filter(id=record.org_id).first()
                            person = Person.objects.filter(id=record.pers_id).first()

                            # Check if related objects exist before creating the association
                            if massnahme and organisation and person:
                                MassnahmeOrganisation.objects.create(
                                    massnahme=massnahme,
                                    organisation=organisation,
                                    person=person
                                )
                                print(f"Created MassnahmeOrganisation for Massnahme {record.kuerzel_massnahme}, Organisation {record.org_id}, Person {record.pers_id}")
                            else:
                                print(f"Missing related objects for record: {record}")
                    except Exception as e:
                        print(f"Error processing record {record}: {e}")
        

        #generate_codes()
        #BusinessObject.objects.all().delete()
        #generate_themen()
        #generate_handlungsfelder()
        #generate_ziele()
        generate_massnahmen()
        #generate_personen()
        #generate_organisationen()
        generate_org_massnahme_beziehung()

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data.'))
