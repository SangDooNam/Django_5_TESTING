"""Notes URL Configuration."""
from django.urls import path
from django.views.generic import TemplateView

from notes.views import (AddNoteView, EditNoteView, NoteDetails,
                         NotesBySection, SearchView, SectionList, VoteNoteView,
                         home)

app_name = "notes"
urlpatterns = [
    path('', home, name="home"),
    path('sections/', SectionList.as_view(), name="sections"),
    path('sections/<section_name>/', NotesBySection.as_view(), name="by_section"),
    path('<int:note_id>/', NoteDetails.as_view(), name="details"),
    path('<int:note_id>/edit/', EditNoteView.as_view(), name="edit"),
    path('<int:note_id>/vote/', VoteNoteView.as_view(), name="vote"),
    path('search/', SearchView.as_view(), name="search"),
    path('add/ok', TemplateView.as_view(template_name="notes/note_added.html"), name="added_ok"),
    path('add/', AddNoteView.as_view(), name="add"),
]
