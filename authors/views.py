from django.shortcuts import render
from .models import Author
from books.models import Book

def author(request, key):
    author = Author.objects.get(id=key)
    id = author.id
    publications = Book.objects.filter(id__exact=key)

    context = {
        "author": author,
        "publications": publications
    }

    return render(request, "author-page.html", context)
