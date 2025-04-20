from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_dairy = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.title