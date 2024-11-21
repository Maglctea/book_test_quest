from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class ExportBooksTask(models.Model):
    class TaskStatus(models.TextChoices):
        COMPLETED = 'COMPLETED'
        IN_PROGRESS = 'IN_PROGRESS'
        FAILED = 'FAILED'
        READY = 'READY'

    status = models.CharField(max_length=100, choices=TaskStatus.choices, default=TaskStatus.READY, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    filepath = models.CharField(max_length=150, null=True, blank=True)
