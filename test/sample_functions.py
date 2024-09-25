from books_service.models import Book


def sample_book(**kwargs):
    book_data = {
        "title": "Test_title",
        "author": "test_author",
        "cover": "SOFT",
        "inventory": 1,
        "daily_fee": 10
    }
    print(kwargs)
    for key, value in kwargs.items():
        book_data.update({key: value})

    return Book.objects.create(
        author=book_data["author"],
        title=book_data["title"],
        cover=book_data["cover"],
        inventory=book_data["inventory"],
        daily_fee=book_data["daily_fee"]
    )
