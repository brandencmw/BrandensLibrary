from django.shortcuts import render
from django.db.models import Q
from .models import Book, Tag
from django.http import HttpResponse



def home(request):
    recently_added = Book.objects.all().order_by("created")[:7:-1]
    context = {
        "recently_added":recently_added
    }

    return render(request, "index.html", context)

def search(request):
    search_terms = request.GET["search-terms"].split(" ")
    results = []
    for term in search_terms:
        query_set = Book.objects.filter(title__contains=term)
        for result in query_set:
            if result not in results:
                results.append(result)

    context = {'search_results': results}
    return render(request, "search-results.html", context)

def book(request, key):
    book = Book.objects.get(id=key)
    author = book.author
    tags = book.tags.all()
    context = {'book': book, 'author':author, 'tags':tags}
    return render(request, "single-book.html", context)


def valid_query(param):
    return param != "" and param is not None

def browse(request):
    books = Book.objects.all()

    author_name_query = request.GET.get('author_name')
    len_start_query = request.GET.get('len_range_start')
    len_end_query = request.GET.get('len_range_end')
    pub_start_query = request.GET.get('pub_range_start')
    pub_end_query = request.GET.get('pub_range_end')
    fiction_query = request.GET.get('fiction_check')
    nonfiction_query = request.GET.get('nonfiction_check')
    tag_query = request.GET.getlist('tag_list')

    if valid_query(author_name_query):
        books = books.filter(Q(author__first_name__icontains=author_name_query) | Q(author__last_name__icontains=author_name_query))

    if valid_query(len_start_query):
        books = books.filter(length__gte=len_start_query)

    if valid_query(len_end_query):
        books = books.filter(length__lte=len_end_query)

    if valid_query(pub_start_query):
        books = books.filter(publish_year__gte=pub_start_query)
    
    if valid_query(pub_end_query):
        books = books.filter(publish_year__lte=pub_end_query)

    if nonfiction_query is None and fiction_query is not None:
        books = books.filter(category="f")
    elif fiction_query is None and nonfiction_query is not None:
        books = books.filter(category="nf")

    if tag_query != []:
        books = books.filter(tags__name__in=tag_query)

    context = {
        'books':books.distinct(),
        'tags':Tag.objects.all()
    }

    return render(request, "browse-books.html", context)


        

