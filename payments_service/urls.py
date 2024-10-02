from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payments_service.views import PaymentViewSet

router = DefaultRouter()

router.register("", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "payments_service"
