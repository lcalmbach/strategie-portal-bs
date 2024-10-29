from django import forms
from .models import PlanRecord, Person, Organisation, Handlungsfeld, Ziel, Massnahme, MassnahmeOrganisation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit



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
             'rueckmeldung_austausch': forms.CheckboxInput(),
        }


class PlanRecordForm(forms.ModelForm):
    class Meta:
        model = PlanRecord
        exclude = ['rueckmeldung_fgs','rueckmeldung_sp', 'erstellt_von', 'erstellt_am', 'massnahme', 'jahr', 'verantwortlich', 'organisation']
        widgets = {
            'rueckmeldung_austausch': forms.CheckboxInput(),
            'einhaltung_termin': forms.CheckboxInput(),
            'umsetzung_mv': forms.Textarea(attrs={'class': 'textarea-wide'}),
            'einhaltung_termin': forms.Select(),
            'einhaltung_termin_text': forms.Textarea(attrs={'class': 'textarea-wide'}),
            'rueckmeldung_mv': forms.Textarea(attrs={'class': 'textarea-wide'}),
            'zufriedenheit_umsetzung': forms.Select(),
        }

    def __init__(self, group_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_only = False
        # Massnahmenverantwortliche, Status-MV gesetzt
        if group_name == 'mv' and getattr(self.instance, 'status_id', 'unbekannt') >= 18:
            disabled_fields = self.fields
            self.read_only = True
        elif group_name == 'sp':
            disabled_fields = [field_name for field_name in self.fields if field_name not in ['status', 'rueckmeldung_sp']]
        elif group_name == 'sp' and getattr(self.instance, 'status_id', 'unbekannt') == 19:
            disabled_fields = self.fields
            self.read_only = True
        elif group_name == 'fgs':
            disabled_fields = [field_name for field_name in self.fields if field_name != 'rueckmeldung_fgs']
        else:
            disabled_fields = []
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'  
        self.helper.form_tag = True

        jahr = getattr(self.instance.massnahme, 'termin', 'unbekannt') 
        messbarkeit = getattr(self.instance.massnahme, 'mess_groesse', 'unbekannt') 
        self.helper.layout = Layout(
            Fieldset(
                f'Termin für die Umsetzung der Massnahme: {jahr}',
                'einhaltung_termin', 
                Field('einhaltung_termin_text', css_class='textarea-wide'),

            ),
             Fieldset(
                f'Messbarkeit der Massnahme: {messbarkeit}',
                'stand_umsetzung', 
                Field('umsetzung_mv', css_class='textarea-wide'), 
                'zufriedenheit_umsetzung',
            ),
            Fieldset(
                'Allgemeine Rückmeldungen',
                'rueckmeldung_austausch', 
                Field('rueckmeldung_mv', css_class='textarea-wide'), 
                'status',
            ),
        )

        # Conditionally add the submit button if the form is not read-only
        if not self.read_only:
            self.helper.add_input(Submit('submit', 'Speichern', css_class='btn btn-primary'))

        for field in disabled_fields:
            self.fields[field].disabled = True



class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = '__all__'

