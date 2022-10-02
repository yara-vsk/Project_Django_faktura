from .models import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, inch
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, Paragraph
from reportlab.platypus.tables import colors, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from slownie import *

import datetime

styles = getSampleStyleSheet()
reportlab.rl_config.warnOnMissingFontGlyphs = 0
pdfmetrics.registerFont(TTFont('Timess', './media/times.ttf'))
pdfmetrics.registerFont(TTFont('Timess_bd', './media/TIMESBD.ttf'))


def numb_f(numb):
    string_numb=str(round(numb, 2))
    index_i=0
    for i in string_numb:
        if i is ".":
            index_i=string_numb.index(i)
    if len(string_numb)-index_i==2:
        string_numb=string_numb+'0'
    return string_numb.replace('.',',')


def name_element_zawijanie(name,count):
    lists = name.split()
    list_n = ''
    lists_s = [x for x in lists]
    y = 0
    z = False
    for i in range(len(lists)):
        if len(list_n) + len(lists[i]) + y <= 50:
            list_n = list_n + lists[i]
            y = y + 1
        else:
            if lists_s[i - 1] == '':
                z = True
                continue
            if z:
                lists_s[i - 1] = '\n' + lists[i - 1] + '\n' + lists[i]
            else:
                lists_s[i - 1] = lists[i - 1] + '\n' + lists[i]
            list_n = lists[i]
            lists_s[i] = ''
            y = 0
            z = False
    return " ".join([x for x in lists_s if x != ""])

def sets_vat(myFaktura_id):
    list_vat=[]
    for element in Faktura_elementy.objects.filter(faktura_id=myFaktura_id):
        list_vat.append(element.element_sprzedazy.vat)
    return set(list_vat)


def text_pdf(mycanvas,id_f, data_user):
    CompanyData = data_user[0]
    myFaktura=Faktura.objects.get(pk=id_f)
    textobject = mycanvas.beginText()
    mycanvas.translate(0,11*inch)
    textobject.setTextOrigin(3.535*inch, 11*inch)
    textobject.setFont("Timess", 12)
    data1 = [['Faktura'],
             [f'nr {myFaktura.number}']]
    t1 = Table(data1, 3.535*2 * inch)
    t1.setStyle(TableStyle([
        #('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 0), (-1, -1), "Timess_bd"),
        ('FONTSIZE', (0, 0), (0, 0), 14),
        ('FONTSIZE', (-1, -1), (-1, -1), 14),
    ]))
    data2 = [['Sprzedawca:','', 'Nabywca:'],
            [f'{name_element_zawijanie(CompanyData.name,45)}\nul. {CompanyData.adres}\n{CompanyData.kod} {CompanyData.miasto}\nNIP: {CompanyData.nip}',
             '',
             f'{name_element_zawijanie(myFaktura.company.name,45)}\nul. {myFaktura.company.adres}\n{myFaktura.company.kod} {myFaktura.company.miasto}\nNIP: {myFaktura.company.nip}'],
            ['', '', ''],
            [f'Data wystawienia: {myFaktura.data_wystawienia}\nMiejsce wystawienia: {myFaktura.miejsce_wystawienia}\nData dostawy/wykonania usługi: {myFaktura.data_wykonania}',
             '',
              f'Termin płatności: {myFaktura.data_wystawienia + datetime.timedelta(days=myFaktura.termin_platnosci)} ({(myFaktura.termin_platnosci)} dni)\nSposób płatności: {myFaktura.sposob_platnosci}\n{data_user[2]}\n{data_user[1]}']]
    t2 = Table(data2,(3.135*inch,0.8*inch, 3.135*inch))
    t2.setStyle(TableStyle([
        #('LINEABOVE', (0,0), (-1,0), 1, colors.black),
        ('FONT', (0,1), (-1,-1), "Timess"),
        ('FONT', (0, 0), (-1, 0), "Timess_bd"),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
        #('LINEABOVE', (0, -2), (-1, -2), 0.5, colors.black),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
    ]))
    data_x = [
        ['L.p.', 'Nazwa', 'Jednostka', 'Ilość', 'Cena\nnetto', 'Wartość\nnetto', 'Stawka\nVAT', 'Kwota\nVAT\n(PLN)',
         'Wartość\nbrutto']]

    numb_element=0

    for element in Faktura_elementy.objects.filter(faktura_id=myFaktura.id):
        numb_element =numb_element+1
        wartosc_netto=element.element_sprzedazy.cena_jednostkowa * element.element_sprzedazy.count
        kwota_vat=round(wartosc_netto*element.element_sprzedazy.vat/100,2)
        brutto=wartosc_netto+kwota_vat
        name_element=name_element_zawijanie(element.element_sprzedazy.name,50)
        p = Paragraph(
            f"<align='center'><wordWrap><font face='Timess' size=7>{name_element_zawijanie(name_element, 50)}</font></wordWrap></align>")

        data_x.append([f'{numb_element}',
                       p,
                       f'',
                       f'{element.element_sprzedazy.count}',
                       f'{numb_f(element.element_sprzedazy.cena_jednostkowa)}',
                       f'{numb_f(wartosc_netto)}',
                       f'{element.element_sprzedazy.vat}%',
                       f'{numb_f(kwota_vat)}',
                       f'{numb_f(brutto)}'])

    for x in range(1):
        name_element=" ".join(['wk'*24 for x in range(4)])
        p=Paragraph(f"<align='center'><wordWrap><font face='Timess' size=7>{name_element_zawijanie(name_element, 50)}</font></wordWrap></align>")

    y=0
    suma_elem=[0,0,0]
    for i in sets_vat(myFaktura.id):
        wartosc_netto=0
        kwota_vat=0
        brutto=0
        opis='W tym'
        for element in Faktura_elementy.objects.filter(faktura_id=myFaktura.id):
            if element.element_sprzedazy.vat==i:
                wartosc_netto=wartosc_netto+element.element_sprzedazy.cena_jednostkowa * element.element_sprzedazy.count
            kwota_vat = round(wartosc_netto*element.element_sprzedazy.vat/100,2)
            brutto = wartosc_netto + kwota_vat
        if y>=1:
            opis=''
        y=y+1
        suma_elem[0]=suma_elem[0]+wartosc_netto
        suma_elem[1] = suma_elem[1] + kwota_vat
        suma_elem[2] = suma_elem[2] + brutto
        data_x.append([f'',
                       f'',
                       f'',
                       f'',
                       f'{opis}',
                       f'{numb_f(wartosc_netto)}',
                       f'{i}%',
                       f'{numb_f(kwota_vat)}',
                       f'{numb_f(brutto)}'])

    data_x.append([f'',
                   f'',
                   f'',
                   f'',
                   f'RAZEM',
                   f'{numb_f(suma_elem[0])}',
                   f'',
                   f'{numb_f(suma_elem[1])}',
                   f'{numb_f(suma_elem[2])}'])

    t3 = Table(data_x, ( 0.37*inch, 2.5*inch, 0.6*inch, 0.6*inch,0.6*inch,0.6*inch,0.6*inch,0.6*inch,0.6*inch))
    t3.setStyle(TableStyle([
        # ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 1), (-1, -2), "Timess"),
        ('FONT', (0, 0), (-1, 0), "Timess_bd"),
        ('FONT', (0, -1), (-1, -1), "Timess_bd"),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        #('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        #('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]))

    data4 = [[f'Razem słownie: {slownie(int(suma_elem[2]//1))} PLN {int(suma_elem[2]%1*100)}/100\nZapłacono: 0,00 PLN\nPozostało do zapłaty: {numb_f(suma_elem[2])} PLN']
             ]
    if suma_elem[2]>15000:
        data4.append(['Mechanizm podzielonej płatności'])

    t4 = Table(data4, 3.535 * 2 * inch)
    t4.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), "Timess"),
        ('FONTSIZE', (0, 0), (-1, -1), 8)
    ]))

    data5 = [['', '', ''],
             ['', '', ''],
             ['Imię, nazwisko i podpis osoby upoważnionej do\nodebrania dokumentu', '',
              'Imię, nazwisko i podpis osoby upoważnionej do\nwystawienia dokumentu']]
    t5 = Table(data5, (3.135 * inch, 0.8 * inch, 3.135 * inch))
    t5.setStyle(TableStyle([
        ('FONT', (0, -1), (-1, -1), "Timess"),
        ('FONT', (0, 0), (-1, -2), "Timess_bd"),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, -1), (-1, -1), 7),
        ('FONTSIZE', (0, 0), (-1, -2), 8),
    ]))

    w, h1 = t1.wrapOn(mycanvas, 0.6*inch, 0.01*inch)
    t1.drawOn(mycanvas, 0.6 * inch, -0.25*inch)
    w, h2 = t2.wrapOn(mycanvas, 0.6 * inch, 1.4 * inch)
    t2.drawOn(mycanvas, 0.6 * inch, -h2-0.6*inch)
    w, h3 = t3.wrapOn(mycanvas, 0.6 * inch, 1 * inch)
    t3.drawOn(mycanvas, 0.6 * inch, -h2-h3-0.9*inch)
    w, h4 = t4.wrapOn(mycanvas, 0.6 * inch, 1 * inch)
    t4.drawOn(mycanvas, 0.6 * inch, -h4-h3-h2-1 * inch)
    w, h5 = t5.wrapOn(mycanvas, 0.6 * inch, 1 * inch)
    h_p=-h4-h5-h2-h3-1.5 * inch
    if (-1)*h_p>=10*inch:
        t5.drawOn(mycanvas, 0.6 * inch, -h4 - h5 - h2 - h3 - 1.5 * inch)
    else:
        t5.drawOn(mycanvas, 0.6 * inch, -10 * inch)

    textobject.textLines(f'''

             ''')
    mycanvas.drawText(textobject)

    textobject2 = mycanvas.beginText()
    textobject2.setTextOrigin(0.5 * inch, 7 * inch)
    textobject2.setFont("Timess", 10)
    #textobject2.textLines(f'''
         #elementy sprzedazy:
         #''')

    #for element in Faktura_elementy.objects.filter(faktura_id=myFaktura.id):
        #textobject2.textLines(f'    Name:{element.element_sprzedazy.name}')
        #textobject2.textLines(f'    Cena jednostkowa: {element.element_sprzedazy.cena_jednostkowa} zł')
       # textobject2.textLines('')
    #mycanvas.drawText(textobject2)


def create_pdf(id_faktura, data_user):
    c = canvas.Canvas(f"media/faktura_{id_faktura}.pdf")
    #company = Company.objects.get(user.krs)
    text_pdf(c,id_faktura, data_user)
    c.showPage()
    c.save()