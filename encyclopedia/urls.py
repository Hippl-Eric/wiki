from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create_ent, name="create_ent"),
    path("wiki/<str:entry_name>/edit", views.edit_ent, name="edit_ent"),
    path("random_ent", views.random_ent, name="random_ent"),
]
