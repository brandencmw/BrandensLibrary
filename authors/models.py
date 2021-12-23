from django.db import models
from uuid import uuid4

class Author(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    headshot = models.ImageField(null=True, blank=True, default="default.jpg")

    def __str__(self):
        return self.first_name + " " + self.last_name

