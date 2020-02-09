from django.db import models

class Report(models.Model):
    title = models.CharField(max_length=50)
    query = models.CharField(max_length=65000)
    created = models.DateTimeField()
