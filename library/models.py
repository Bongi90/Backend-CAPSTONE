from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(null=True, blank=True)
    copies_available = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} by {self.author}"

class Transaction(models.Model):
    STATUS_CHOICES = [
        ("OUT", "Checked Out"),
        ("RETURNED", "Returned"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="transactions")
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="OUT")

    class Meta:
        ordering = ["-checkout_date"]
        constraints = [
            models.UniqueConstraint(fields=["user", "book", "status"], condition=models.Q(status="OUT"), name="unique_active_checkout_per_user_book"),
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.book.title} ({self.status})"
