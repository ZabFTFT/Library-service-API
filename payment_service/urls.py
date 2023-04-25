from django.urls import path, include
from rest_framework import routers

from payment_service.views import PaymentView

router = routers.DefaultRouter()
router.register("payments", PaymentView, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "payment_service"
