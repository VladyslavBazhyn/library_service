from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import viewsets

from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingBaseSerializer, BorrowingListSerializer, BorrowingDetailSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        serializer_class = BorrowingListSerializer
        if self.action == "list":
            serializer_class = BorrowingListSerializer
        if self.action == "retrieve":
            serializer_class = BorrowingDetailSerializer

        return serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                type=int,
                name="user_id"
            ),
            OpenApiParameter(
                type=bool,
                name="is_active"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Optionally restricts the returned borrowings,
        by filtering against a user id and whether borrowing is still active or not.
        """
        queryset = self.queryset

        if self.request.query_params.get("user_id", None):
            user_id = self.request.query_params.get("user_id")
            queryset = queryset.filter(user_id=user_id)

        if self.request.query_params.get("is_active", None):
            status = self.request.query_params.get("is_active")
            queryset = queryset.filter(is_active=status)

        return queryset
