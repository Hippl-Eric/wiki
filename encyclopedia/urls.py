from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create_ent", views.create_ent, name="create_ent"),
    path("random_ent", views.random_ent, name="random_ent"),
]
