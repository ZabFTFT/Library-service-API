from django.urls import path, include
from rest_framework import routers
from borrowing_service.views import BorrowingsViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet, basename="borrowing")

urlpatterns = [path("", include(router.urls))]

app_name = "borrowing_service"
