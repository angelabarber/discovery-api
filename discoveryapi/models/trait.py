from django.db import models


class Trait(models.Model):
    name = models.CharField(max_length=255)
    category_name = models.CharField(max_length=255)
