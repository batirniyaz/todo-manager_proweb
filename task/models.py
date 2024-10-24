from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Task(models.Model):
    PENDING = 'P'
    IN_PROGRESS = 'IP'
    COMPLETED = 'C'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed')
    ]

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True, null=True, max_length=255)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    due_date = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasks')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.due_date and self.due_date < timezone.now():
            raise ValidationError('Due date cannot be in the past.')

    def __str__(self):
        return self.title
