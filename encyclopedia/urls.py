from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("random", views.get_random_entry, name="random"),
    path("edit/<str:entry_title>/", views.edit, name="edit"),
    path("<str:title>", views.entry, name="entry")
]