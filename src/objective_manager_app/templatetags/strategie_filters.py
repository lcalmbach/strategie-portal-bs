# templatetags/strategie_filters.py

from django import template
from ..models import BusinessObject, Strategie, MassnahmeOrganisation, Person

register = template.Library()

@register.filter(name='handlungsfelder')
def handlungsfelder(strategie):
    return BusinessObject.objects.filter(typ_id=2, strategie=strategie)

@register.filter(name='ziele')
def ziele(strategie):
    return BusinessObject.objects.filter(typ_id=3, strategie=strategie)

@register.filter(name='massnahmen')
def massnahmen(strategie):
    return BusinessObject.objects.filter(typ_id=4, strategie=strategie)

@register.filter(name='personen')
def massnahmen(strategie):
    return Person.objects.filter(
        massnahmeorganisation__massnahme__strategie=strategie
    ).distinct()