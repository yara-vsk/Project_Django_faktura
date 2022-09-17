from django.contrib import admin
from django.urls import path, include
from .views import get_name, get_data, get_pdf_faktura, get_krs_kontrahent,get_dane_firmy


urlpatterns = [
    path('', get_data),
    path('custom_kontrahent/', get_name),
    path('new_kontrahent/', get_krs_kontrahent),
    path('<int:link>/', get_pdf_faktura),
    path('dane_firmy/<str:krs>/', get_dane_firmy),
]
