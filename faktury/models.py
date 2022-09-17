from django.db import models
from django.utils.translation import gettext_lazy as _



class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    nip=models.CharField(unique=True, max_length=10)
    krs = models.CharField(unique=True, max_length=10)
    miasto= models.CharField(max_length=45)
    kod=models.CharField(max_length=45)
    adres=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ElementSprzedazy(models.Model):
    class JednostkaSpz(models.TextChoices):
        j1 = 'usł.', _('usługa')
        j2 = 'h', _('godzina')
        j3 = 'kpl.', _('komplet')
        j4 = 'szt.', _('sztuka')
        j5 = 'm', _('metr')
        j6 = 'm2', _('metr kwadratowy')
        j7 = 'm3', _('metr sześcienny')

    class StawkiVat(models.IntegerChoices):
        v1 = 23, _('23%')
        v2 = 8, _('8%')
        v3 = 5, _('5%')
        v4 = 0, _('0%')

    name = models.CharField(max_length=200)
    jednostka =models.CharField(max_length=50,choices=JednostkaSpz.choices, default=JednostkaSpz.j1)
    count = models.IntegerField()
    cena_jednostkowa=models.FloatField()
    vat = models.IntegerField(choices=StawkiVat.choices, default=StawkiVat.v1)

    def __str__(self):
        return self.name


class Faktura(models.Model):
    class MetodyPlatnosci(models.TextChoices):
        m1 = 'przelew na rachunek bankowy', _('przelew na rachunek bankowy')
        m2 = 'gotówka', _('gotówka')
        m3 = 'karta płatnicza', _('karta płatnicza')
    number = models.CharField(max_length=20, unique=True)
    data_wystawienia=models.DateField()
    miejsce_wystawienia=models.CharField(max_length=45)
    data_wykonania=models.DateField()
    sposob_platnosci=models.CharField(max_length=45,choices=MetodyPlatnosci.choices, default=MetodyPlatnosci.m2)
    termin_platnosci=models.IntegerField()
    elementy_sprzedazy=models.ManyToManyField(ElementSprzedazy, through='Faktura_elementy')
    company=models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.number


class Faktura_elementy(models.Model):
    faktura_id = models.ForeignKey(Faktura, on_delete=models.CASCADE)
    element_sprzedazy = models.ForeignKey(ElementSprzedazy, on_delete=models.CASCADE)

