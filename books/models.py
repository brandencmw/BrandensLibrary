from django.db import models
from uuid import uuid4
from authors.models import Author
from tags.models import Tag

class Book(models.Model):
    BOOK_CATEGORY = (
        ("f", "Fiction"),
        ("nf", "Non Fiction"),
        ("hf", "Historical Fiction")
    )

    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    publish_year = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=200, choices=BOOK_CATEGORY, null=True, blank=True)
    authors = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tag, blank=True)
    cover_img = models.ImageField(null=True, blank=True, default="default.jpg")

    def __str__(self):
        return self.title

