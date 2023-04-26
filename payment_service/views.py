import stripe
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from flask import app, Flask
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, HttpResponseBadRequest

from config import settings
from payment_service.models import Payment
from payment_service.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
)


app = Flask(__name__)


class PaymentView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Payment.objects.all()
        user = get_user_model().objects.get(id=self.request.user.id)
        if not user.is_staff:
            queryset = Payment.objects.filter(
                borrowing__customer=self.request.user
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        if self.action == "create":
            pass
        return PaymentSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY

endpoint_secret = settings.ENDPOINT_SECRET

LAST_SESSION_ID = ""
LAST_SESSION_URL = ""


def checkout(request):
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": "price_1N0pheIuU04V0CJIMycb5x0R",
                "quantity": 50,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )
    global LAST_SESSION_URL
    global LAST_SESSION_ID
    LAST_SESSION_URL = session["url"]
    LAST_SESSION_ID = session["id"]

    return redirect(session.url, code=303)


@csrf_exempt
@app.route("/webhook", methods=["POST"])
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        pass

    return HttpResponse(status=200)
