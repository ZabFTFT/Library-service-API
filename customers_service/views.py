from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from customers_service.serializers import (
    CustomerManageSerializer,
    AuthTokenSerializer,
    CustomerCreateSerializer,
    CustomerChangePasswordSerializer,
)


class CreateCustomerView(generics.CreateAPIView):
    serializer_class = CustomerCreateSerializer


class ManageCustomerView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerManageSerializer

    def get_object(self):
        return self.request.user


class ChangeCustomerPasswordView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerChangePasswordSerializer

    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer
