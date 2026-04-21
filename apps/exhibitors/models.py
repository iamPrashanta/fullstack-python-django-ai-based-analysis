from django.db import models

class Exhibitor(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    hall = models.CharField(max_length=50)
    booth = models.CharField(max_length=50)
    sector = models.TextField()
    logo_url = models.URLField()

    def __str__(self):
        return self.name