from django.db import models


class Book(models.Model):
    class BookCover(models.TextChoices):
        hard = "HARD"
        soft = "SOFT"

    Title = models.CharField(max_length=100, unique=True)
    Author = models.CharField(max_length=100)
    Cover = models.TextField(choices=BookCover)
    Inventory = models.PositiveIntegerField()
    Daily_fee = models.DecimalField(decimal_places=5, max_digits=10)
