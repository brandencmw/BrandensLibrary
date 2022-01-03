from django.shortcuts import render
from books.models import Book
from .models import Tag

def tag(request, key):
    tag = Tag.objects.get(id=key)
    books = Book.objects.filter(tags__name__in=[tag])
    context = {
        "tag":tag,
        "books":books
    }

    return render(request, "tag-page.html", context)