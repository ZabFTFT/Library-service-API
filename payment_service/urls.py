from django.urls import path, include
from rest_framework import routers


from payment_service.views import PaymentView, checkout, my_webhook_view


router = routers.DefaultRouter()
router.register("payments", PaymentView, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("checkout/", checkout, name="checkout"),
    path("webhook/", my_webhook_view, name="webhook"),
]


app_name = "payment_service"
