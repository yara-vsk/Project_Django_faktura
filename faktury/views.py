from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .form import NameCompanyForm, FakturaForm, CompanyForm, ElementSprzedazyForm, ElementSprzedazyFormSet, KrsForm
from .models import *
from .pdfcreator import create_pdf
from datetime import date
from django.forms import inlineformset_factory
import requests
import json


def krs_searching(krs):
    res=requests.get(f'https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{krs}?rejestr=P&format=json')
    try:
        u=json.loads(res.text)
    except json.decoder.JSONDecodeError:
        return {}
    try:
        data_c = u.get('odpis').get('dane').get('dzial1')
    except AttributeError:
        return {}
    if data_c:
        try:
            adres = data_c['siedzibaIAdres']['adres']['ulica'] + " " + data_c['siedzibaIAdres']['adres']['nrDomu'] + '/' + \
                    data_c['siedzibaIAdres']['adres']['nrLokalu']
        except KeyError:
            try:
                adres = data_c['siedzibaIAdres']['adres']['ulica'] + " " + data_c['siedzibaIAdres']['adres']['nrDomu']
            except KeyError:
                adres = data_c['siedzibaIAdres']['adres']['nrDomu']

        try:
            data_company = {
                'name': data_c['danePodmiotu']['nazwa'],
                'nip': data_c['danePodmiotu']['identyfikatory']['nip'],
                'krs': krs,
                'miasto': data_c['siedzibaIAdres']['adres']['miejscowosc'],
                'kod': data_c['siedzibaIAdres']['adres']['kodPocztowy'],
                'adres': adres,
            }
        except KeyError:
            return {}
    else:
        return {}
    return data_company


def company_create(krs):
    data_c = krs_searching(krs)
    if data_c:
        Company.objects.create(
            name=data_c['name'],
            nip=data_c['nip'],
            krs=data_c['krs'],
            miasto=data_c['miasto'],
            kod=data_c['kod'],
            adres=data_c['adres']
        )
    return Company.objects.filter(krs=krs)


def test_func(user):
    if Company.objects.filter(krs=user.krs):
        return True
    else:
        company_create(user.krs)
        return Company.objects.filter(krs=user.krs)


@login_required(login_url='/login')
def get_krs_kontrahent(request):
    if request.method == 'POST':
        form = KrsForm(request.POST)
        if form.is_valid():
            krs=form.cleaned_data['krs']
            company_data=krs_searching(krs)
            if company_data:
                company_create(krs)
                return redirect(f'/faktury/dane_firmy/{krs}')
            else:

                form.add_error(None, "Please, enter correct KRS")
    else:
        form = KrsForm()
    return render(request, 'faktury/kontrahentKrs.html', {'form': form})


@login_required(login_url='/login')
@user_passes_test(test_func, login_url='/faktury/add_data_company/user')
def get_dane_firmy(request,krs):
    if krs == "user":
        krs = request.user.krs
    firma=Company.objects.get(krs=krs)
    return render(request, 'faktury/dane_firmy.html', {'form':firma})


@login_required(login_url='/login')
def create_company_manually(request, option):
    add_information = False
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            Company.objects.create(
                name=form.cleaned_data['name'],
                nip=form.cleaned_data['nip'],
                krs=form.cleaned_data['krs'],
                miasto=form.cleaned_data['miasto'],
                kod=form.cleaned_data['kod'],
                adres=form.cleaned_data['adres']
            )
            if option =='user':
                print(request.user)
                request.user.krs=form.cleaned_data['krs']
                request.user.save()
            return redirect(f'/')
    else:
        form = CompanyForm()
        if option =='user':
            add_information = True
    return render(request, 'faktury/kontrahent.html', {'form': form,'inf':add_information})


@login_required(login_url='/login')
@user_passes_test(test_func, login_url='/')
def get_data(request):
    if request.method == 'POST':
        form1 = FakturaForm(request.POST)
        formset = ElementSprzedazyFormSet(request.POST)
        if form1.is_valid() and formset.is_valid():
            faktura_new=Faktura.objects.create(
                number=form1.cleaned_data['number'],
                data_wystawienia=form1.cleaned_data['data_wystawienia'],
                data_wykonania=form1.cleaned_data['data_wykonania'],
                sposob_platnosci=form1.cleaned_data['sposob_platnosci'],
                termin_platnosci = form1.cleaned_data['termin_platnosci'],
                company=form1.cleaned_data['company'],
                miejsce_wystawienia = form1.cleaned_data['miejsce_wystawienia']

            )
            for form in formset:
                element_new=ElementSprzedazy.objects.create(
                    name=form.cleaned_data['name'],
                    count=form.cleaned_data['count'],
                    cena_jednostkowa=form.cleaned_data['cena_jednostkowa'],
                    vat=form.cleaned_data['vat'],
                    jednostka = form.cleaned_data['jednostka'],
                )
                faktura_new.elementy_sprzedazy.add(element_new)
            return redirect(f'{faktura_new.id}/')
    else:
        form1 = FakturaForm()
        formset = ElementSprzedazyFormSet()
    return render(request, 'faktury/elementy.html', {'form1': form1,'formset': formset})


@login_required(login_url='/login')
@user_passes_test(test_func, login_url='/')
def get_pdf_faktura(request,link):
    company=Company.objects.get(krs=request.user.krs)
    create_pdf(link, company)
    return render(request, 'faktury/download.html',{'cont':link})
