from django.conf import settings
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator


class SmartPassword(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='smart_passwords',
        blank=True,
        null=True
    )
    description = models.CharField(max_length=255)

    length = models.PositiveSmallIntegerField(
        default=16,
        validators=[
            MinValueValidator(12, message="Password length must be at least 12 characters"),
            MaxValueValidator(100, message="Password length cannot exceed 100 characters")
        ]
    )
    public_key = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['public_key']),
            models.Index(fields=['description']),
        ]

    def __str__(self):
        return self.description
