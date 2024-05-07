from django.db import models
from django.contrib.auth.models import User
from .artifact import Artifact


class Comment(models.Model):
    artifact = models.ForeignKey(
        Artifact, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField
