from django.shortcuts import render
from .models import Author
from books.models import Book

def author(request, key):
    author = Author.objects.get(id=key)
    publications = Book.objects.filter(author__id=key)

    context = {
        "author": author,
        "publications": publications
    }

    return render(request, "author-page.html", context)
