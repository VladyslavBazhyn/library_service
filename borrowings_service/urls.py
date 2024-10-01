from django.urls import path

from borrowings_service.views import BorrowingReturnView, BorrowingListView, BorrowingDetailView, \
    BorrowingCreateView


urlpatterns = [
    path("", BorrowingListView.as_view(), name="list"),
    path("create/", BorrowingCreateView.as_view(), name="create"),
    path("<int:pk>/", BorrowingDetailView.as_view(), name="borrowing-detail"),
    path("<int:pk>/return/", BorrowingReturnView.as_view({"post": "return_borrowing"}), name="borrowing-return"),

]

app_name = "borrowings_service"
