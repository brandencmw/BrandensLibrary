from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('search-results/', views.search, name="search"),
    path('book-info/<str:key>', views.book, name="book-info"),
    path('browse', views.browse, name="browse-books")
]