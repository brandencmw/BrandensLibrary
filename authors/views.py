from django.shortcuts import render
from .models import Author
from books.models import Book
import requests

def author(request, key):
    author = Author.objects.get(id=key)
    author_id = author.id
    publications = Book.objects.filter(authors__id__in=[author_id])

    query = author.first_name + author.last_name
    api_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
            "action":"query",
            "format":"json",
            "list":"search",
            "utf8":1,
            "srsearch":query
        }
 
    data = requests.get(api_url, params=search_params).json()
    print(data)
    top_result = data["query"]["search"][0]["title"]
    retrieve_params = {
            "action": "query",
            "format": "json",
            "titles": top_result,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
        }

    response = requests.get(api_url, params=retrieve_params)
    data = response.json()
    bio = next(iter(data['query']['pages'].values()))["extract"]
    link = "https://en.wikipedia.org/wiki/" + "_".join(top_result.split())

    context = {
        "author": author,
        "bio": bio,
        "link":link,
        "publications": publications
    }

    return render(request, "author-page.html", context)
