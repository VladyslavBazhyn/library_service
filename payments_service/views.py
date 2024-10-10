import stripe
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payments_service.models import Payment
from payments_service.serializers import PaymentBaseSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentBaseSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user_id=self.request.user.pk)

        return queryset
