from django.contrib import admin
from .models import BusinessObject, Code, Strategie, Person, Organisation, StrategieDokument


# Register the BusinessObject model with a custom admin class if needed
@admin.register(BusinessObject)
class BusinessObjectAdmin(admin.ModelAdmin):
    list_display = (
        'kuerzel',
        'titel',
        'typ',
        'vorgaenger',
        'erstellt_am',
        'erstellt_von',
    )
    search_fields = ('titel', 'kuerzel', 'beschreibung')
    list_filter = ('typ', 'erstellt_am', 'erstellt_von')

@admin.register(Strategie)
class Strategie(admin.ModelAdmin):
    list_display = (
        'titel',
        'gueltigkeit_jahr_start',
        'gueltigkeit_jahr_ende',
    )
    search_fields = ('titel',)

@admin.register(Organisation)
class Strategie(admin.ModelAdmin):
    list_display = (
        'departement',
        'dienststelle',
        'bereich',
    )
    search_fields = ('departement','dienststelle','bereich')

@admin.register(Person)
class Strategie(admin.ModelAdmin):
    list_display = (
        'vorname',
        'nachname',
        'organisation',
    )
    search_fields = ('vorname','nachname')

@admin.register(StrategieDokument)
class StrategieDokument(admin.ModelAdmin):
    list_display = (
        'strategie',
        'titel_dokument',
        'url_feld',
    )
    search_fields = ('strategie','titel_dokument', 'url_feld')


admin.site.register(Code)
