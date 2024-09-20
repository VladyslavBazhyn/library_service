from django.db import models


class Book(models.Model):
    class BookCover(models.TextChoices):
        hard = "HARD"
        soft = "SOFT"

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.TextField(choices=BookCover)
    daily_fee = models.DecimalField(decimal_places=5, max_digits=10)
    available = models.BooleanField(default=True)
