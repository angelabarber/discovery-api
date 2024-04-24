from django.db import models
from django.contrib.auth.models import User
from .site import Site


class Artifact(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="artifacts")
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="artifacts")
    traits = models.ManyToManyField(
        "Trait", through="ArtifactTrait", related_name="artifacts"
    )
