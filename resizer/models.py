from django.db import models


# Create your models here.
class ProcessedTasks(models.Model):
    task_id = models.CharField(max_length=100, blank=False)
