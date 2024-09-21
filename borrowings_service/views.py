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
