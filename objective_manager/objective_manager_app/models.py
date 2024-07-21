from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class CodeKategorie(models.Model):
    titel = models.CharField(max_length=100)
    beschreibung = models.CharField(max_length=200)

    def __str__(self):
        return self.kategorie



class Code(models.Model):
    kategorie = models.ForeignKey(CodeKategorie, on_delete=models.CASCADE)
    kuerzel = models.CharField(max_length=10)
    titel = models.CharField(max_length=10)
    beschreibung = models.CharField(max_length=200)

    def __str__(self):
        return self.titel

class ThemaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=1)
    
class HandlungsfeldManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=2, vorgaenger__typ_id=1)

class ZielManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=3, vorgaenger__typ_id=2)

class MassnahmeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=4, vorgaenger__typ_id=3)
    
class BusinessObject(models.Model):
    typ = models.ForeignKey(Code, on_delete=models.CASCADE)
    vorgaenger = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    kuerzel = models.CharField(max_length=10)
    titel = models.CharField(max_length=200, verbose_name="Titel")
    beschreibung = models.TextField(verbose_name="Beschreibung")
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    erstellt_von = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Erstellt von")
    aufwand_personen_tage_plan = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aufwand Personentage", default=0)
    aufwand_tsd_chf_plan = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Aufwand tsd CHF", default=0)
    jahr_start = models.IntegerField(verbose_name="Jahr Start", default=datetime.now().year)
    jahr_ende = models.IntegerField(verbose_name="Jahr Ende", default=datetime.now().year)

    objects = models.Manager()
    themen = ThemaManager()
    handlungsfelder = HandlungsfeldManager()
    ziele = ZielManager()
    massnahmen = MassnahmeManager()

    def __str__(self):
        return self.titel
    
class Handlungsfeld(BusinessObject):
    objects = HandlungsfeldManager()

    class Meta:
        proxy = True


class Ziel(BusinessObject):
    objects = ZielManager()

    class Meta:
        proxy = True


class Massnahme(BusinessObject):
    objects = MassnahmeManager()

    class Meta:
        proxy = True


class thema(models.Model):
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField()
    kontakt = models.CharField(max_length=200)
    jahr_start = models.IntegerField(verbose_name="Jahr Start", default = datetime.now().year +1)    
    jahr_ende = models.IntegerField(verbose_name="Jahr Ende", default = datetime.now().year + 5)    


    def __str__(self):
        return self.titel


class PlanRecord(models.Model):
    objekt = models.ForeignKey(BusinessObject, on_delete=models.CASCADE,verbose_name="Massnahme")
    organisation = models.ForeignKey(Code, on_delete=models.CASCADE, verbose_name="Organisation")
    jahr = models.IntegerField(verbose_name="Jahr", default=datetime.now().year)
    monat = models.IntegerField()
    soll_wert_erreicht_pzt = models.IntegerField(verbose_name="Zielerreichungsgrad (Soll, %)")
    ist_wert_erreicht_pzt = models.IntegerField(verbose_name="Zielerreichungsgrad (Ist, %)")
    aufwand_personen_tage_plan = models.IntegerField(verbose_name='Aufwand Personentage (Soll)')
    aufwand_tsd_chf_plan = models.IntegerField(verbose_name='Aufwand tsd CHF (Soll)')
    aufwand_personen_tage_ist = models.IntegerField(default=0, verbose_name='Aufwand Personentage (Ist)')
    aufwand_tsd_chf_ist = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Aufwand tsd CHF (Ist)')
    beschreibung = models.TextField(verbose_name="Beschreibung")
    erstellt_am = models.DateTimeField(auto_now_add=True,verbose_name='Erstellt am')
    erstellt_von = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Erstellt von')

    def __str__(self):
        return f"{self.objekt.titel} {self.jahr}"
