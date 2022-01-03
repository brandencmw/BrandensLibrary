from django.urls import path
from . import views

urlpatterns = [
    path('tag/<str:key>', views.tag, name="tag-page"),
]