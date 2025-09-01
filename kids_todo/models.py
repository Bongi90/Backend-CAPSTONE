from django.db import models
from django.contrib.auth.models import User

class TaskTemplate(models.Model):
    BEFORE = "BEFORE"
    AFTER = "AFTER"
    CATEGORY_CHOICES = [(BEFORE, "Before School"), (AFTER, "After School")]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=BEFORE)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "order"]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class DailyTask(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_tasks")
    date = models.DateField()
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=TaskTemplate.CATEGORY_CHOICES, default=TaskTemplate.BEFORE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("owner", "date", "title", "category")
        ordering = ["category", "id"]

    def __str__(self):
        return f"{self.title} - {self.date} ({self.owner.username})"
