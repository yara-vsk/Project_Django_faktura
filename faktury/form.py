from django import forms
from django.forms import ModelForm
from .models import Faktura, Company, ElementSprzedazy
from django.forms import formset_factory, BaseFormSet, inlineformset_factory
from django.utils.translation import gettext_lazy as _


class NameCompanyForm(forms.Form):
    name = forms.CharField(label='Name of company', max_length=300)

class FakturaForm(ModelForm):
    class Meta:
        model = Faktura
        fields= ['number', 'sposob_platnosci', 'data_wykonania', 'termin_platnosci','company','data_wystawienia','miejsce_wystawienia']
        labels = {
            'number': _('Numer faktury'),
            'sposob_platnosci': _('Sposób platności'),
            'data_wykonania': _('Data wykonania'),
            'data_wystawienia': _('Data wystawienia'),
            'termin_platnosci': _('Termin platności'),
            'company': _('Nabywca'),
            'miejsce_wystawienia': _('Miejsce wystawienia'),
        }


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields= ['name','nip','krs','miasto', 'kod', 'adres' ]
        labels = {
            'name': _('Nazwa pełna'),
            'nip': _('NIP'),
            'krs': _('Numer KRS'),
            'miasto': _('Miasto'),
            'kod': _('Kod pocztowy'),
            'adres': _('Ulica dom / lokal'),
        }


class KrsForm(ModelForm):
    class Meta:
        model = Company
        fields= ['krs']
        labels = {
            'krs': _('Numer KRS'),
        }


class ElementSprzedazyForm(ModelForm):
    class Meta:
        model = ElementSprzedazy
        fields= ['name','count','cena_jednostkowa', 'vat', 'jednostka']
        labels = {
            'name': _('Nazwa'),
            'count': _('Ilość'),
            'cena_jednostkowa': _('Cena netto'),
            'vat': _('VAT'),
            'jednostka': _('Jednostka'),
        }


ElementSprzedazyFormSet = formset_factory(ElementSprzedazyForm,can_delete_extra=True)
