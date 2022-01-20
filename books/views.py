from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.contrib.postgres.aggregates import StringAgg
from .models import Book, Tag
from django.http import HttpResponse



def home(request):
    recently_added = Book.objects.all().order_by("created")[:7:-1]
    context = {
        "recently_added":recently_added
    }

    return render(request, "index.html", context)

def search(request):
    query = SearchQuery(request.GET["search-terms"], search_type="websearch")
    vector = SearchVector("title", weight="A") + \
        SearchVector("description", weight="B") + \
        SearchVector(StringAgg("authors__last_name", delimiter=" "), weight="C") + \
        SearchVector(StringAgg("authors__first_name", delimiter=" "), weight="C") + \
        SearchVector(StringAgg("tags__name", delimiter=" "), weight="B")

    results = Book.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.1).order_by("-rank")
    print(results)
    context = {
        "search_results": results
    }
    return render(request, "search-results.html", context)

def book(request, key):
    book = Book.objects.get(id=key)
    authors = book.authors.all()
    tags = book.tags.all()
    context = {'book': book, 'authors':authors, 'tags':tags}
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

    if request.GET.get('inlineRadioOptions') is not None:
        sort_query = int(request.GET.get('inlineRadioOptions')[-1])
    else:
        sort_query = 3


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

    if sort_query < 3:
        sort = "title"
    elif sort_query < 5:
        sort = "authors__last_name"
    elif sort_query < 7:
        sort = "publish_year"
    else:
        sort = "length"
    
    if sort_query % 2 == 0:
        sort = "-" + sort
    
    books = books.order_by(sort)

    context = {
        'books':books.distinct(),
        'tags':Tag.objects.all()
    }

    return render(request, "browse-books.html", context)


        

