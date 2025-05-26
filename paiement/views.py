import requests
import uuid
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Remplace par tes vraies clés
SITE_ID = "votre_site_id"
API_KEY = "votre_api_key"
CINETPAY_URL = "https://api-checkout.cinetpay.com/v2/payment"

@csrf_exempt
def payer(request):
    transaction_id = str(uuid.uuid4())

    data = {
        "transaction_id": transaction_id,
        "amount": "1000",
        "currency": "XOF",
        "channels": "TMoney",
        "description": "Paiement test TMoney",
        "site_id": SITE_ID,
        "apikey": API_KEY,
        "return_url": "https://exemple.ngrok.io/paiement/success/",  # ngrok ici
        "notify_url": "https://exemple.ngrok.io/paiement/webhook/",
        "customer_name": "Client test",
        "customer_email": "test@example.com"
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(CINETPAY_URL, json=data, headers=headers)
    result = response.json()

    if result.get("code") == "201":
        payment_url = result.get("data").get("payment_url")
        return JsonResponse({"payment_url": payment_url})
    else:
        return JsonResponse({"error": result}, status=400)

def paiement_success(request):
    return HttpResponse("✅ Paiement effectué avec succès (retour utilisateur).")

@csrf_exempt
def webhook(request):
    print("📡 Webhook reçu")
    print(request.body)  # Tu peux sauvegarder cela en base plus tard
    return HttpResponse("OK")
