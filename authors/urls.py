from django.urls import path
from . import views


urlpatterns = [
    path('author-page/<str:key>', views.author, name="author-page"),
]