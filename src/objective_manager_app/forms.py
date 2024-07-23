from django import forms
from .models import BusinessObject, PlanRecord, Person
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

class PlanRecordForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        exclude = ['objekt']
        exclude = ['organisation']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'