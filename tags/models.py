from django.db import models
from uuid import uuid4

class Tag(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

