
from django.db import models
from core.models import TimestampedModel

class MLModelRegistry(TimestampedModel):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50) # e.g. v1.0.0
    s3_path = models.CharField(max_length=1024)
    is_active = models.BooleanField(default=False)
    metrics = models.JSONField(default=dict) # Evaluation metrics
    parameters = models.JSONField(default=dict) # Training parameters

    class Meta:
        unique_together = ('name', 'version')

    def __str__(self):
        return f"{self.name} - {self.version}"
