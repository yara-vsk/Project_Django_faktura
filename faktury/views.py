from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .form import FakturaForm, CompanyForm, ElementSprzedazyFormSet, KrsForm
from .models import *
from .pdfcreator import create_pdf
from .companycreator import company_create, krs_searching, test_func


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
@user_passes_test(test_func, login_url='/faktury/add_data_company/user')
def get_data(request):
    if request.method == 'POST':
        form1 = FakturaForm(request.POST)
        formset = ElementSprzedazyFormSet(request.POST)
        company_user = Company.objects.get(krs=request.user.krs)
        b_number = request.user.B_account_number
        b_name = request.user.Bank_name
        if form1.is_valid() and formset.is_valid():
            faktura_new=Faktura.objects.create(
                number=form1.cleaned_data['number'],
                data_wystawienia=form1.cleaned_data['data_wystawienia'],
                data_wykonania=form1.cleaned_data['data_wykonania'],
                sposob_platnosci=form1.cleaned_data['sposob_platnosci'],
                termin_platnosci = form1.cleaned_data['termin_platnosci'],
                company_buy=form1.cleaned_data['company_buy'],
                company_sell=company_user,
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

            create_pdf(faktura_new.id, (company_user, b_number, b_name))
            return redirect(f'download/{faktura_new.id}/')
    else:
        form1 = FakturaForm()
        formset = ElementSprzedazyFormSet()
    return render(request, 'faktury/elementy.html', {'form1': form1,'formset': formset})


@login_required(login_url='/login')
@user_passes_test(test_func, login_url='/faktury/add_data_company/user')
def get_pdf_faktura(request,link):
    company_user=Company.objects.get(krs=request.user.krs)
    queryset=Faktura.objects.filter(id=link)
    context = ""
    if queryset:
        if queryset[0].company_sell==company_user:
            context = f"media/Faktura_{link}_{'1'.join([x for x in (company_user.krs) if x != '0'])}.pdf"
        else:
            raise Http404
    else:
        raise Http404
    return render(request, 'faktury/download.html',{'cont':context})


@login_required(login_url='/login')
@user_passes_test(test_func, login_url='/faktury/add_data_company/user')
def get_faktury_list_view(request):
    queryset = Faktura.objects.filter(company_sell=Company.objects.get(krs=request.user.krs).id)
    return render(request, 'faktury/faktury_list.html', {'object_list': queryset})
