from django import forms
from .models import PlanRecord, Person, Organisation, Handlungsfeld, Ziel, Massnahme, MassnahmeOrganisation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class HandlungsfeldForm(forms.ModelForm):
    class Meta:
        model = Handlungsfeld
        exclude = ['erstellt_von', 'strategie', 'typ', 'vorgaenger', 'aufwand_personen_tage_plan','aufwand_tsd_chf_plan','jahr_start','jahr_ende','anmerkung_initialisierung','bestehende_massnahme']
        

class ZielForm(forms.ModelForm):
    class Meta:
        model = Ziel
        exclude = ['erstellt_von', 'strategie', 'typ', 'vorgaenger', 'anmerkung_initialisierung','bestehende_massnahme']


class MassnahmeForm(forms.ModelForm):
    class Meta:
        model = Massnahme
        exclude = ['erstellt_von', 'strategie', 'typ', 'vorgaenger']


class MassnahmeOrganisationForm(forms.ModelForm):
    class Meta:
        model = MassnahmeOrganisation
        exclude = ['massnahme']


class PlanRecordFGSForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        fields = ['bemerkungen_fgs']

class PlanRecordSPForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        fields = ['status', 'bemerkungen_sp']

class PlanRecordMVForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        fields = ['status', 'bemerkungen_code_mv', 'rueckmeldung_mv', 'einhaltung_termin', 'umsetzung_mv', 'fortschritt', 'zufriedenheit', 'schwierigkeiten']
        

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = '__all__'

