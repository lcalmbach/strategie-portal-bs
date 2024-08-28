from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
from django.contrib.auth.models import User

class CodeKategorie(models.Model):
    titel = models.CharField(max_length=100)
    beschreibung = models.CharField(max_length=200)

    def __str__(self):
        return self.kategorie


class Organisation(models.Model):
    departement = models.CharField(max_length=200, verbose_name='Departement')
    dienststelle = models.CharField(max_length=200, verbose_name='Dienststelle')
    bereich = models.CharField(max_length=200, verbose_name='Bereich')
    departement_kuerzel = models.CharField(max_length=200, verbose_name='Departement Kürzel')
    dienststelle_kuerzel = models.CharField(max_length=200, verbose_name='Dienststelle Kürzel')
    bereich_kuerzel = models.CharField(max_length=200, verbose_name='Bereich Kürzel')
    
    def __str__(self):
        return self.bereich if self.bereich else self.dienststelle

    class Meta:
        ordering = ['departement_kuerzel', 'dienststelle'] 


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    vorname = models.CharField(verbose_name= 'Vorname', max_length=200)
    nachname = models.CharField(verbose_name= 'Nachname', max_length=200)
    email = models.EmailField(verbose_name= 'Email', max_length=200, null=True, blank=True)
    telefon = models.CharField(verbose_name= 'Telefon', max_length=200, null=True, blank=True)
    organisation = models.ForeignKey(Organisation, verbose_name='Organisation', on_delete=models.CASCADE)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nachname', 'vorname'] 

    def vorname_nachname(self):
        return f"{self.vorname} {self.nachname}"
    
    def nachname_vorname(self):
        return f"{self.nachname} {self.vorname}"
    
    def __str__(self):
        return f"{self.nachname} {self.vorname}"


class BusinessObjectTypManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=1)


class HandlungsfeldManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=2)


class ZielManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=3)
    

class MassnahmeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(typ_id=4)
    

class BusinessObjectTypManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=1)


class NeuBestehendManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=2)


class RueckmeldungMVManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=4)


class RolleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=3)
    
        
class WertungManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=5)


class StatusMassnahmeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=6)

class ZufriedenheitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=7)
    
class JaNeinManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(kategorie_id=8)


    
class Code(models.Model):
    kategorie = models.ForeignKey(CodeKategorie, on_delete=models.CASCADE)
    kuerzel = models.CharField(max_length=10)
    titel = models.CharField(max_length=10)
    beschreibung = models.CharField(max_length=200)
    color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.titel


class BusinessObject(models.Model):
    typ = models.ForeignKey("BusinessObjectTyp", on_delete=models.CASCADE, related_name="typ")
    vorgaenger = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    kuerzel = models.CharField(max_length=10, verbose_name="Nummer")
    titel = models.CharField(max_length=200, verbose_name="Titel")
    beschreibung = models.TextField(verbose_name="Beschreibung")
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    erstellt_von = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Erstellt von", blank=True)
    
    jahr_ende = models.IntegerField(verbose_name="Termin", default=datetime.now().year)
    anmerkung_initialisierung = models.TextField(verbose_name="Pol. Vorstoss", null=True, blank=True)
    mess_groesse = models.CharField(max_length=200, verbose_name="Messbarkeit", blank=True, null=True)
    # messbarkeit = models.CharField(max_length=200, verbose_name="Messbarkeit")  
    bestehende_massnahme = models.ForeignKey("NeuBestehend", on_delete=models.CASCADE, blank=True, null=True, default=5, related_name="bestehende_massnahme", verbose_name="Bestehende/Neue Massnahme")

    objects = models.Manager()
    handlungsfelder = HandlungsfeldManager()
    ziele = ZielManager()
    massnahmen = MassnahmeManager()
    
    def __str__(self):
        return self.titel
    
    
class MassnahmeOrganisation(models.Model):
    """
    Eine Klasse, die die Beziehung zwischen einer Massnahme, einer Organisation und einer Person repräsentiert.

    Attribute:
        massnahme (ForeignKey): Eine Fremdschlüsselbeziehung zu einem BusinessObject-Objekt.
        organisation (ForeignKey): Eine Fremdschlüsselbeziehung zu einem Organisation-Objekt.
        person (ForeignKey): Eine Fremdschlüsselbeziehung zu einem Person-Objekt.
        bemerkungen (TextField): Ein optionales Textfeld für Bemerkungen.
        rolle (ForeignKey): Eine Fremdschlüsselbeziehung zu einem Rolle-Objekt.

    Methoden:
        __str__(): Gibt den Titel der Massnahme zurück.
    """
    massnahme = models.ForeignKey(BusinessObject, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=1)
    bemerkungen = models.TextField(max_length=500, verbose_name="Bemerkungen", null=True, blank=True)
    rolle = models.ForeignKey("Rolle", on_delete=models.CASCADE, default=7)

    def __str__(self):
        return self.massnahme.titel


class Rolle(Code):
    objects = RolleManager()

    class Meta:
        proxy = True


class Wertung(Code):
    objects = WertungManager()

    class Meta:
        proxy = True


class StatusMassnahme(Code):
    objects = StatusMassnahmeManager()

    class Meta:
        proxy = True


class BusinessObjectTyp(Code):
    objects = BusinessObjectTypManager()

    class Meta:
        proxy = True


class RueckmeldungMV(Code):
    objects = RueckmeldungMVManager()

    class Meta:
        proxy = True


class NeuBestehend(Code):
    objects = NeuBestehendManager()

    class Meta:
        proxy = True



class JaNein(Code):
    objects = JaNeinManager()

    class Meta:
        proxy = True



class Zufriedenheit(Code):
    objects = ZufriedenheitManager()

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


class PlanRecord(models.Model):
    massnahme = models.ForeignKey(Massnahme, on_delete=models.CASCADE)
    jahr = models.IntegerField(verbose_name="Jahr", default=datetime.now().year)
    verantwortlich = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Massnahmenverantwortliche Person", null=True, blank=True, related_name='planrecord_person')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, verbose_name="Federführende Organisation", null=True, blank=True, related_name='planrecord_organisation')

    rueckmeldung_austausch = models.BooleanField(verbose_name="Austausch oder Beratung ist erwünscht", null=True, default=False)
    rueckmeldung_schwierigkeiten = models.BooleanField(verbose_name="Umsetzung der Massnahme bereitet Schwierigkeiten", null=True, default=False)
    rueckmeldung_neupriorisierung = models.BooleanField(verbose_name="Neupriorisierung von departemententalen Zielen", null=True, default=False)
    rueckmeldung_pol_vorstoss = models.BooleanField(verbose_name="Politischer Vorstoss hat Auswirkungen auf die Massnahme", null=True, default=False)
    rueckmeldung_anderes = models.BooleanField(verbose_name="Anderes", null=True, default=False)
    rueckmeldung_anderes_text = models.TextField(verbose_name="Anderes", max_length=500, null=True, blank=True)

    rueckmeldung_mv = models.TextField(verbose_name="Allgmeine Bemerkungen", null=True, blank=True)
    
    einhaltung_termin = models.ForeignKey(JaNein, verbose_name="Termin wird eingehalten", on_delete=models.CASCADE, null=True, blank=True, related_name='planrecord_einhaltung_termin')
    einhaltung_termin_text = models.TextField(verbose_name="Begründung der Abweichung", max_length=500, null=True, blank=True)
    umsetzung_mv = models.TextField(verbose_name="Welche Schritte, Teilprojekte oder Meilensteine wurden im Berichtsjahr umgesetzt?", null=True, blank=True)
    
    zufriedenheit = models.ForeignKey(Zufriedenheit, verbose_name="Wie zufrieden sind Sie mit der Umsetzung der Massnahme", null=True, blank=True, on_delete=models.CASCADE, related_name='planrecord_zufriedenheit')
    schwierigkeiten = models.ForeignKey(Wertung, verbose_name="Schwierigkeiten", null=True, blank=True, on_delete=models.CASCADE, related_name='planrecord_schwierigkeiten')
    
    rueckmeldung_fgs = models.TextField(verbose_name="Bemerkungen FGS", null=True, blank=True)
    rueckmeldung_sp = models.TextField(verbose_name="Bemerkungen SP", null=True, blank=True)
    status = models.ForeignKey(StatusMassnahme,verbose_name="Status", null=True, default=17, on_delete=models.CASCADE)
    
    erstellt_am = models.DateTimeField(auto_now_add=True, verbose_name='Erstellt am')
    erstellt_von = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Erstellt von')

    def __str__(self):
        return f"{self.verantwortlich.titel} {self.jahr}"