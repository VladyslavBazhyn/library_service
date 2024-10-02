from rest_framework.reverse import reverse

from books_service.models import Book
from borrowings_service.models import Borrowing


def get_book_detail_url(pk: int) -> str:
    return reverse("books_service:book-detail", args=[pk])


def sample_book(**kwargs):
    book_data = {
        "title": "Test_title",
        "author": "test_author",
        "cover": "SOFT",
        "inventory": 1,
        "daily_fee": 10
    }

    for key, value in kwargs.items():
        book_data.update({key: value})

    return Book.objects.create(
        author=book_data["author"],
        title=book_data["title"],
        cover=book_data["cover"],
        inventory=book_data["inventory"],
        daily_fee=book_data["daily_fee"]
    )


def sample_borrowing(**kwargs):
    borrowing_data = {
        "book": sample_book(),
        "expected_return_date": "2025-01-01",
        "user_id": None
    }
    for key, value in kwargs.items():
        borrowing_data.update({key: value})

    return Borrowing.objects.create(
        book=borrowing_data["book"],
        expected_return_date=borrowing_data["expected_return_date"],
        user_id=borrowing_data["user_id"]
    )

