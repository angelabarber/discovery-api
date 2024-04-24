from django.db import models
from .artifact import Artifact
from .trait import Trait


class ArtifactTrait(models.Model):
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE)
