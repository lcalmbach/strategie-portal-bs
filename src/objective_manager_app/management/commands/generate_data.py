import random
from django.core.management.base import BaseCommand
from objective_manager_app.models import CodeKategorie, Code, BusinessObject, Person, Organisation
from django.contrib.auth.models import User
from faker import Faker
import pandas as pd
import os
from django.conf import settings

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
            for organisation in organisation_df.itertuples():
                print(organisation)
                Organisation.objects.create(
                    id=organisation.id,
                    departement=organisation.departement,
                    bereich=organisation.bereich,
                    dienststelle=organisation.dienststelle,

                    departement_kuerzel=organisation.departement_kuerzel,
                    bereich_kuerzel=organisation.bereich_kuerzel,
                    dienststelle_kuerzel=organisation.dienststelle_kuerzel
                )


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
            massnahmen_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'massnahmen.csv')
            massnahmen_df = pd.read_csv(massnahmen_filename, sep=';')
            for massnahme in massnahmen_df.itertuples():
                BusinessObject.objects.create(
                    typ=Code.objects.get(id=4),
                    vorgaenger=BusinessObject.objects.get(kuerzel=massnahme.ziel),
                    titel=massnahme.titel,
                    beschreibung=massnahme.beschreibung,
                    erstellt_von=User.objects.first(),
                    kuerzel=massnahme.kuerzel

                )
        

        #generate_codes()
        #BusinessObject.objects.all().delete()
        #generate_themen()
        #generate_handlungsfelder()
        #generate_ziele()
        #generate_massnahmen()
        #generate_personen()
        generate_organisationen()

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data.'))
