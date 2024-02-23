"""Custom template tags and filters."""

from django import template
from django.urls import reverse
from notes.models import NoteStore
from django.utils.html import mark_safe

register = template.Library()

store = NoteStore()
notes = store.get()


@register.simple_tag
def vote_options(request, note_id):
    """Return the user voting options."""
    options = []
    user_votes = request.session.get("user_votes", [])
    user = request.session.get("user_name", None)
    if user:
        note_obj = notes[note_id - 1]
        section = note_obj["section"]
        vote_in_section = [id + 1 for id, note in enumerate(notes)
                           if note["section"] == section and id + 1 in user_votes]
        try:
            voted_id = vote_in_section.pop(0)
        except IndexError:
            voted_id = None
        if voted_id and voted_id != note_id:
            options = ["You already voted note number ",
                       str(voted_id), "."]
        elif voted_id and voted_id == note_id:
            options = ['You already voted this note.']
        else:
            options = ["<a href=\"",
                       reverse("notes:vote", args=[note_id]),
                       "\">Vote this note</a>."]
    else:
        options = ["You are not allowed to vote. "
                   "<a href=\"", reverse("login"), "\">Log in</a>",
                   " to gain access."]
    return mark_safe("".join(options))
