from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.fees, name='fees'),
    path('receipt/<int:payment_id>/', views.download_receipt, name='download_receipt'),
    path('certificate/<int:payment_id>/', views.download_certificate, name='download_certificate'),
    path('confirm/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
]