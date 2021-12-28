from django.shortcuts import render
from .models import Book
from django.http import HttpResponse



def home(request):
    return render(request, "index.html")

def search(request):
    search_terms = request.GET["search-terms"].split(" ")
    results = []
    for term in search_terms:
        query_set = Book.objects.filter(title__contains=term)
        for result in query_set:
            if result not in results:
                results.append(result)

    context = {'search_results': results}
    print(results)
    return render(request, "search-results.html", context)

def book(request, key):
    book = Book.objects.get(id=key)
    author = book.author
    tags = book.tags.all()
    context = {'book': book, 'author':author, 'tags':tags}
    return render(request, "single-book.html", context)
        

