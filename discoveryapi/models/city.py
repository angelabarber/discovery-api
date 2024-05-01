from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    significance = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
