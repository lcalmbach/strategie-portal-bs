from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
from django.contrib.auth.models import User


class CodeKategorie(models.Model):
    titel = models.CharField(max_length=100)
    beschreibung = models.CharField(max_length=200)

    def __str__(self):
        return self.titel


class Organisation(models.Model):
    departement = models.CharField(max_length=200)
    dienststelle = models.CharField(max_length=200)
    bereich = models.CharField(max_length=200)
    departement_kuerzel = models.CharField(max_length=200)
    dienststelle_kuerzel = models.CharField(max_length=200)
    bereich_kuerzel = models.CharField(max_length=200)

    def __str__(self):
        return self.bereich if self.bereich else self.dienststelle

    class Meta:
        ordering = ["departement_kuerzel", "dienststelle"]


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    vorname = models.CharField(verbose_name="Vorname", max_length=200)
    nachname = models.CharField(verbose_name="Nachname", max_length=200)
    email = models.EmailField(
        verbose_name="Email", max_length=200, null=True, blank=True
    )
    telefon = models.CharField(
        verbose_name="Telefon", max_length=200, null=True, blank=True
    )
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nachname", "vorname"]

    def vorname_nachname(self):
        return f"{self.vorname} {self.nachname}"

    def nachname_vorname(self):
        return f"{self.nachname} {self.vorname}"

    def __str__(self):
        return f"{self.nachname} {self.vorname}"


class BusinessObjectTypManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=1)


class RolleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=3)


class WirkungManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=4)


class Code(models.Model):
    kategorie = models.ForeignKey(CodeKategorie, on_delete=models.CASCADE)
    kuerzel = models.CharField(max_length=10)
    titel = models.CharField(max_length=10)
    beschreibung = models.CharField(max_length=200)

    def __str__(self):
        return self.titel


class HandlungsfeldManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=2)


class ZielManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=3)


class MassnahmeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=4)


class BusinessObject(models.Model):
    strategie = models.ForeignKey("Strategie", on_delete=models.CASCADE, related_name="strategie_business_objects")
    typ = models.ForeignKey(
        "BusinessObjectTyp", on_delete=models.CASCADE, related_name="typ"
    )
    vorgaenger = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    kuerzel = models.CharField(max_length=10)
    titel = models.CharField(max_length=500, verbose_name="Titel")
    beschreibung = models.TextField(verbose_name="Beschreibung")
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    erstellt_von = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Erstellt von", blank=True
    )
    aufwand_personen_tage_plan = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Aufwand Personentage", default=0
    )
    aufwand_tsd_chf_plan = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Aufwand tsd CHF", default=0
    )
    jahr_start = models.IntegerField(
        verbose_name="Jahr Start", default=datetime.now().year
    )
    jahr_ende = models.IntegerField(
        verbose_name="Jahr Ende", default=datetime.now().year
    )

    objects = models.Manager()
    handlungsfelder = HandlungsfeldManager()
    ziele = ZielManager()
    massnahmen = MassnahmeManager()

    def __str__(self):
        return self.titel


class StrategieDokument(models.Model):
    strategie = models.ForeignKey(
        "Strategie", on_delete=models.CASCADE, related_name="dokumente"
    )
    titel_dokument = models.TextField(verbose_name="Titel Dokument", max_length=200)
    url_feld = models.URLField(max_length=500, verbose_name="Webseite")

    def __str__(self):
        return self.titel_dokument


class MassnahmeOrganisation(models.Model):
    massnahme = models.ForeignKey(BusinessObject, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=1)
    bemerkungen = models.TextField(
        max_length=500, verbose_name="Bemerkungen", null=True, blank=True
    )

    def __str__(self):
        return self.massnahme.titel


class Wirkung(Code):
    objects = WirkungManager()

    class Meta:
        proxy = True


class Rolle(Code):
    objects = RolleManager()

    class Meta:
        proxy = True


class BusinessObjectTyp(Code):
    objects = BusinessObjectTypManager()

    class Meta:
        proxy = True


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


class Kennzahl(models.Model):
    titel = models.CharField(max_length=200, verbose_name="Titel")
    beschreibung = models.TextField(max_length=2000, verbose_name="Beschreibung")
    thema = models.CharField(
        max_length=200, verbose_name="Thema", null=True, blank=True
    )
    unterthema = models.CharField(
        max_length=200, verbose_name="Unterthema", null=True, blank=True
    )
    url = models.CharField(max_length=1000, verbose_name="URL")

    def __str__(self):
        return self.titel


class Thema(models.Model):
    kuerzel = models.CharField(max_length=10, verbose_name="Kürzel")
    vorgaenger = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    ebene = models.IntegerField(verbose_name="Ebene", default=1)
    wunschrichtung = models.ForeignKey(
        Wirkung,
        verbose_name="Erwünschte Wirkung",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField(max_length=1000)
    sortierung = models.IntegerField(default=0)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    erstellt_von = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titel


class Strategie(models.Model):
    titel = models.CharField(max_length=200, verbose_name="Titel")
    titel_kurz = models.CharField(
        max_length=200, verbose_name="Kurztitel", default="", null=True, blank=True
    )
    organisation = models.ForeignKey("Organisation", on_delete=models.CASCADE)
    kontakt = models.ForeignKey("Person", on_delete=models.CASCADE)
    gueltigkeit_jahr_start = models.IntegerField(
        verbose_name="Jahr Start", default=datetime.now().year + 1
    )
    gueltigkeit_jahr_ende = models.IntegerField(
        verbose_name="Jahr Ende", default=datetime.now().year + 5
    )
    planungs_frequenz_monate = models.IntegerField(
        verbose_name="Planungsfrequenz (Monate)", default=12
    )
    beschreibung_intern = models.TextField(
        verbose_name="Beschreibung für Beteiligte",
        max_length=1000,
        null=True,
        blank=True,
    )
    beschreibung_extern = models.TextField(
        verbose_name="Beschreibung für Externe", max_length=1000, null=True, blank=True
    )
    settings = models.JSONField(
        verbose_name="Einstellungen", null=True, blank=True, default=dict
    )
    home_image = models.TextField(verbose_name="Bildpfad", null=True, blank=True)

    def __str__(self):
        return self.titel


class BusinessObjectThema(models.Model):
    business_object = models.ForeignKey(
        BusinessObject, on_delete=models.CASCADE, related_name="themen_business_objects"
    )
    thema = models.ForeignKey(
        Thema, on_delete=models.CASCADE, related_name="business_objects_themen"
    )
    wirkung = models.ForeignKey(
        Wirkung, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.business_object.titel} {self.thema.titel}"


class BusinessObjectKennzahl(models.Model):
    business_object = models.ForeignKey(
        BusinessObject,
        on_delete=models.CASCADE,
        related_name="kennzahlen_business_objects",
    )
    kennzahl = models.ForeignKey(
        Kennzahl, on_delete=models.CASCADE, related_name="business_objects_kennzahlen"
    )

    def __str__(self):
        return f"{self.business_object.titel} {self.thema.titel}"


class PlanRecord(models.Model):
    strategie = models.ForeignKey(Strategie, on_delete=models.CASCADE)
    verantwortlich = models.ForeignKey(
        MassnahmeOrganisation, on_delete=models.CASCADE, verbose_name="Massnahme"
    )
    objekt = models.ForeignKey(BusinessObject, on_delete=models.CASCADE)
    jahr = models.IntegerField(verbose_name="Jahr", default=datetime.now().year)
    monat = models.IntegerField()
    beginn_datum = models.DateField(verbose_name="Beginn am", blank=True, null=True)
    ende_datum = models.DateField(verbose_name="Fällig am", blank=True, null=True)
    fortschritt_pzt_plan = models.IntegerField(
        verbose_name="Zielerreichungsgrad (Soll, %)"
    )
    fortschritt_pzt_ist = models.IntegerField(
        verbose_name="Zielerreichungsgrad (Ist, %)", default=0
    )
    aufwand_personen_tage_plan = models.IntegerField(
        verbose_name="Aufwand Personentage (Soll)", default=20
    )
    aufwand_personen_tage_ist = models.IntegerField(
        default=0, verbose_name="Aufwand Personentage (Ist)"
    )
    aufwand_tsd_chf_plan = models.IntegerField(
        verbose_name="Aufwand tsd CHF (Soll)", default=0
    )
    aufwand_tsd_chf_ist = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Aufwand tsd CHF (Ist)"
    )
    kommentar = models.TextField(verbose_name="Kommentar", null=True, blank=True)

    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    erstellt_von = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Erstellt von"
    )

    def __str__(self):
        return f"{self.objekt.titel} {self.jahr}"