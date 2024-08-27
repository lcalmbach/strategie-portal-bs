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


class PlanRecordAdminForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        fields = '__all__'
        widgets = {
            'faellig_am': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date input
        }

class PlanRecordFGSForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        fields = ['rueckmeldung_fgs']

class PlanRecordSPForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        fields = ['status', 'rueckmeldung_sp']

class PlanRecordMVForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        fields = ['status',
                  'rueckmeldung_austausch', 
                  'rueckmeldung_schwierigkeiten', 
                  'rueckmeldung_neupriorisierung',
                  'rueckmeldung_pol_vorstoss',
                  'rueckmeldung_anderes',
                  'rueckmeldung_anderes_text',   
                  'rueckmeldung_mv', 
                  'einhaltung_termin', 
                  'umsetzung_mv', 
                  'zufriedenheit', 
                  'schwierigkeiten'
            ]
        widgets = {
            'einhaltung_termin': forms.CheckboxInput(),
            'rueckmeldung_austausch': forms.CheckboxInput(),
            'rueckmeldung_schwierigkeiten': forms.CheckboxInput(),
            'rueckmeldung_neupriorisierung': forms.CheckboxInput(),
            'rueckmeldung_pol_vorstoss': forms.CheckboxInput(),
            'rueckmeldung_anderes': forms.CheckboxInput()
        }
        

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = '__all__'

