from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import viewsets, status, generics, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings_service.models import Borrowing
from borrowings_service.serializers import BorrowingBaseSerializer, BorrowingListSerializer, BorrowingDetailSerializer, \
    BorrowingReturnSerializer, BorrowingCreateSerializer


class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingListSerializer

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
        """Adding extended schema for better documentation."""
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Optionally restricts the returned borrowings,
        by filtering against a user id and whether borrowing is still active or not.
        """
        queryset = Borrowing.objects.all()

        if self.request.query_params.get("user_id", None):
            user_id = self.request.query_params.get("user_id")
            queryset = queryset.filter(user_id=user_id)

        if self.request.query_params.get("is_active", None):
            borrowing_status = self.request.query_params.get("is_active")
            queryset = queryset.filter(is_active=borrowing_status)

        if self.request.user.is_staff is not True:
            """Non admin users should see only theirs borrowings"""
            queryset = queryset.filter(user_id=self.request.user.pk)

        return queryset


class BorrowingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BorrowingDetailSerializer
    queryset = Borrowing.objects.all()


class BorrowingReturnView(viewsets.ModelViewSet):
    serializer_class = BorrowingReturnSerializer
    queryset = Borrowing.objects.all()

    def return_borrowing(self, request, pk):
        """
        Custom action to handle returning the borrowing
        """
        try:
            borrowing = Borrowing.objects.get(id=pk)
        except Borrowing.DoesNotExist:
            return Response({"error": "Borrowing not found."}, status=status.HTTP_404_NOT_FOUND)

        # Make sure that borrowing still active
        if borrowing.is_active:
            borrowing.is_active = False
            borrowing.save()
        else:
            return Response({"error": "Borrowing not active."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the book's inventory
        book = borrowing.book
        book.inventory += 1
        book.save()

        # Use the BorrowingReturnSerializer to update the actual_return_date
        serializer = BorrowingReturnSerializer(borrowing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BorrowingCreateView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingCreateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
