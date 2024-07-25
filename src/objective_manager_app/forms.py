from django import forms
from .models import BusinessObject, PlanRecord, Person, Organisation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class BusinessObjectForm(forms.ModelForm):
    class Meta:
        model = BusinessObject
        fields = [
            "typ",
            "vorgaenger",
            "kuerzel",
            "titel",
            "beschreibung",
            "erstellt_von",
        ]

class ZielForm(forms.ModelForm):
    class Meta:
        model = BusinessObject
        exclude = ['erstellt_von','anmerkung_initialisierung','bestehende_massnahme','messbarkeit']


class PlanRecordForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        exclude = ['objekt']
        exclude = ['organisation']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = '__all__'

