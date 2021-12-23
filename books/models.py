from django.db import models
from uuid import uuid4
from authors.models import Author

class Book(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    publish_year = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default="")
    cover_img = models.ImageField(null=True, blank=True, default="default.jpg")

    def __str__(self):
        return self.title

