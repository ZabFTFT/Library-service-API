from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from views import BorrowingsViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet, basename="borrowings")


urlpatterns = [
    path("", include(router.urls))
]

app_name = "borrowing_service"
