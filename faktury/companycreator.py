import json
from .models import *
import requests


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