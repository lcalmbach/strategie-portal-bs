import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from objective_manager_app.models import Massnahme
from django.conf import settings
import random
import string
import os
import pandas as pd


class Command(BaseCommand):
    help = 'Create a user for each person in the Person table'

    def handle(self, *args, **kwargs):
        massnahmen_filename = os.path.join(settings.BASE_DIR, 'objective_manager_app', 'data', 'massnahmen.csv')
        massnahmen_df = pd.read_csv(massnahmen_filename, sep=';')
        massnahmen_df.fillna(0, inplace=True)
        for massnahme in massnahmen_df.itertuples():
            print(massnahme.kuerzel, massnahme.messbarkeit)
            m = Massnahme.objects.filter(kuerzel=massnahme.kuerzel).first()
            m.mess_groesse = massnahme.messbarkeit
            m.save()