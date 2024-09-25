from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


@action(detail=True, methods=["POST"], url_path="return", name="return", url_name="return")
def return_borrowing(request, pk):
    print("Borrowing pk:", pk)
    borrowing = Borrowing.objects.get(id=pk)
    print("Borrowing:", borrowing)
    borrowing.is_active = False
    print("Borrowing is active:", borrowing.is_active)
    borrowing.save()

    book = borrowing.book
    print("Book:", book)
    print("Book inventory:", book.inventory)
    book.inventory += 1
    print("Book inventory:", book.inventory)
    book.save()

    return HttpResponse(status=status.HTTP_200_OK)

from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingBaseSerializer, BorrowingListSerializer, BorrowingDetailSerializer, \
    BorrowingReturnSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        serializer_class = BorrowingListSerializer
        if self.action == "list":
            serializer_class = BorrowingListSerializer
        if self.action == "retrieve":
            serializer_class = BorrowingDetailSerializer
        if self.action == "return_borrowing":
            serializer_class = BorrowingReturnSerializer

        return serializer_class

    # @action(detail=True, methods=["POST"], url_path="return", name="return", url_name="return")
    # def return_borrowing(self, request, pk):
    #     borrowing = Borrowing.objects.get(id=pk)
    #     borrowing.is_active = False
    #     borrowing.save()
    #
    #     book = borrowing.book
    #     book.inventory += 1
    #     book.save()
    #
    #     return Response(status=status.HTTP_200_OK)

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
