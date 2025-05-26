
from django.urls import path
from . import views

urlpatterns = [
    path('payer/', views.payer, name='payer'),
    path('success/', views.paiement_success, name='success'),
    path('webhook/', views.webhook, name='webhook'),
]
