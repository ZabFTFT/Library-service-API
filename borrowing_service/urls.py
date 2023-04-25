from django.urls import path, include
from rest_framework import routers
from borrowing_service.views import BorrowingsListViewSet

router = routers.DefaultRouter()

router.register("borrowings", BorrowingsListViewSet, basename="borrowings")

urlpatterns = [path("", include(router.urls))]

app_name = "borrowing_service"
