"""apitest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apitest.views.api import spreadsheet_to_json, generate_qr_code, generate_barcode

urlpatterns = [
    path("spreadsheet/", spreadsheet_to_json, name="spreadsheet_to_json"),
    path("qrcode/<str:code_data>", generate_qr_code, name="generate_qr_code"),
    path("barcode/<str:barcode_format>/<str:number_code>", generate_barcode, name="generate_barcode"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
