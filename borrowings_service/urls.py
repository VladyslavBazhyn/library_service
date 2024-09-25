from django.urls import path, include
from rest_framework.routers import DefaultRouter

from borrowings_service.views import BorrowingViewSet, return_borrowing

routers = DefaultRouter()

routers.register("", BorrowingViewSet)

urlpatterns = [
    path("/", include(routers.urls)),
    path("<int:pk>/return/", return_borrowing, name="return")
]

app_name = "borrowings_service"
