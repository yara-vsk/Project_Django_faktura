from django.contrib import admin
from django.urls import path, include
from .views import create_company_manually, get_data, get_pdf_faktura, get_krs_kontrahent,get_dane_firmy


urlpatterns = [
    path('', get_data),
    path('add_data_company/<str:option>/', create_company_manually),
    path('new_kontrahent/', get_krs_kontrahent),
    path('<int:link>/', get_pdf_faktura),
    path('dane_firmy/<str:krs>/', get_dane_firmy),
]
