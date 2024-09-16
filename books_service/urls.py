from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books_service.views import BookViewSet

app_name = "book_service"

router = DefaultRouter()

router.register("books", BookViewSet, basename="books")

urlpatterns = [
    path("", include(router.urls))
]
