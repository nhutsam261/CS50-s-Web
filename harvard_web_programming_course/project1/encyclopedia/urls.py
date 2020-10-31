from django.urls import path

from . import views
app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_page, name="title"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random, name="random"),
    path("save/", views.save, name="save"),
]
