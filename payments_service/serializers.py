from rest_framework import serializers

from payments_service.models import Payment


class PaymentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id", "status", "type", "borrowing_id", "session_url", "session_id", "money_to_pay", "user"
        )
