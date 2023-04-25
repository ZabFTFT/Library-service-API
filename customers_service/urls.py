from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from customers_service.views import (
    CreateCustomerView,
    ManageCustomerView,
    ChangeCustomerPasswordView,
)


urlpatterns = [
    path("", CreateCustomerView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageCustomerView.as_view(), name="manage-customer"),
    path(
        "me/change-password/",
        ChangeCustomerPasswordView.as_view(),
        name="manage-password",
    ),
]


app_name = "customers_service"
