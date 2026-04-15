from django.conf import settings
from django.db import models


class Case(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cases",
    )
    form_template = models.ForeignKey(
        "forms_engine.FormTemplate",
        on_delete=models.CASCADE,
        related_name="cases",
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Case #{self.pk} - {self.user}"