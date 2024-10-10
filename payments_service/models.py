from django.contrib.auth import get_user_model
from django.db import models
from unicodedata import decimal

from borrowings_service.models import Borrowing

User = get_user_model()


class Payment(models.Model):
    class StatusChoice(models.TextChoices):
        pending = "PENDING"
        paid = "PAID"

    class TypeChoice(models.TextChoices):
        payment = "PAYMENT"
        fine = "FINE"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.TextField(choices=StatusChoice)
    type = models.TextField(choices=TypeChoice)
    borrowing_id = models.IntegerField()
    session_url = models.TextField()
    session_id = models.TextField()
    # money_to_pay = models.DecimalField(decimal_places=10, max_length=20)

    # @property
    # def money_to_pay(self) -> decimal:
    #     # Find borrowing
    #     borrowing = Borrowing.objects.get(id=self.borrowing_id)
    #
    #     # Calculate how many days this borrowing was active
    #     borrow_date = borrowing.borrow_date
    #     actual_return_date = borrowing.actual_return_date
    #     days_of_borrowing = actual_return_date - borrow_date
    #
    #     # Find daily fee for book of this borrowing
    #     daily_fee = borrowing.book.daily_fee
    #
    #     # Calculate how much money user owes for this borrowing
    #     daily_fee = decimal(daily_fee)
    #     money_to_pay = days_of_borrowing * daily_fee
    #
    #     return money_to_pay
