from drf_spectacular.utils import extend_schema, OpenApiParameter
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
            OpenApiParameter
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

        return queryset
