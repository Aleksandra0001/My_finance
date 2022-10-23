from django.db import models
from django.db.models import ForeignKey
from django.utils.timezone import now
from django.conf import settings


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    description = models.TextField()
    category = models.TextField()
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Owner of incomes",
        on_delete=models.CASCADE,
        related_name='incomes',
    )

    def __str__(self):
        return f"Owner: {self.user_id}, Income: {self.amount}, {self.created_at}, {self.description}, {self.category}"
        # return self.description, self.id  # noQA


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    description = models.TextField()
    category = models.TextField()
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Owner of expenses",
        on_delete=models.CASCADE,
        related_name='expenses',
    )

    def __str__(self):
        return f"Owner: {self.user_id}, Expense: {self.amount}, {self.created_at}, {self.description}, {self.category}"
        # return self.description, self.id  # noQA
