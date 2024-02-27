"""Views for the notes app."""
from django.template.loader import get_template
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View

from notes.models import NoteStore
from common.models import UserStore
from notes.forms import SearchForm, AddNoteForm, EditNoteForm


store = NoteStore()
notes = store.get()


def redirect_to_note_detail(request, note_id):
    """Redirect to the note details view."""
    return redirect(reverse("notes:details", args=[note_id]))


def home(request):
    """Home for my notes app."""
    template = get_template("notes/home.html")
    context = {
        "request": request,
        "title": "Welcome to my course notes!",
        "links": [
            {
                "url": reverse("notes:sections"),
                "label": "Check the list of sections"
            },
            {
                "url": reverse("notes:details", args=[1]),
                "label": "Read my first notes"
            },
            {
                "url": reverse("notes:search"),
                "label": "Search a note"
            },
            {
                "url": reverse("notes:add"),
                "label": "Add a new note"
            }
        ]
    }
    return HttpResponse(template.render(context))


class SectionList(TemplateView):
    """List of sections."""

    template_name = "notes/sections.html"

    def get_context_data(self):
        """Return the list of sections."""
        return {
            "sections": ["Web Frameworks",
                         "Setting up Django",
                         "URL Mapping"]
            }


class NotesBySection(TemplateView):
    """Show the notes of a section."""

    template_name = "notes/by_section.html"

    def get_context_data(self, section_name):
        """Return the section name and the note list."""
        return {
            "section": section_name,
            "notes": _get_notes_by_section(section_name)
        }


def _get_notes_by_section(section_name):
    """Return the notes of a section."""
    return [note for note in notes
            if note["section"] == section_name]


class SearchView(FormView):
    """The search form view."""

    template_name = "notes/search.html"
    form_class = SearchForm

    def get_context_data(self):
        """Get the notes in the context."""
        term = self.request.GET.get("term_of_search", None)
        section = self.request.GET.get("section", None)
        context = super().get_context_data()
        if term:
            matching = notes
            if section:
                matching = [note for note in notes
                            if note["section"] == section]
            context["notes"] = matching
            context["term_of_search"] = term
            context["section"] = section
        return context


class NoteDetails(TemplateView):
    """Note details."""

    template_name = "notes/details.html"

    def get_context_data(self, note_id):
        """Return the note data."""
        note = notes[note_id - 1]
        return {
            "id": note_id,
            "num_notes": len(notes),
            "note": note
        }


def _get_note_items_matching_search(search_term):
    """Return a list of items with notes marching the search."""
    return [f"<li>{note['text']}</li>" for note in notes
            if search_term.lower() in note["text"].lower()]


class AddNoteView(FormView):
    """Input a new note into the system."""

    template_name = "notes/add.html"
    form_class = AddNoteForm
    success_url = reverse_lazy("notes:added_ok")

    def form_valid(self, *args, **kwargs):
        """Save the note in the store."""
        form = self.get_form()
        note = {
            "text": form.data.get("text", None),
            "section": form.data.get("section", None)
        }
        notes.append(note)
        store.save(notes)
        return super().form_valid(*args, **kwargs)


class EditNoteView(FormView):
    """Edit the text of a note."""

    template_name = "notes/edit.html"
    form_class = EditNoteForm

    def get_initial(self):
        """Return the values of the given note_id."""
        note_id = self.kwargs["note_id"]
        return notes[note_id - 1]

    def get_success_url(self):
        """Return the success url."""
        note_id = self.kwargs["note_id"]
        return reverse("notes:details", args=[note_id])

    def form_valid(self, form):
        """Save the data."""
        note_id = self.kwargs["note_id"]
        notes[note_id - 1]["text"] = form.data.get("text")
        return super().form_valid(form)


class VoteNoteView(View):
    """Store a new vote."""

    def get(self, request, note_id):
        """Store the note vote."""
        # Update the note object
        note = notes[note_id - 1]
        note["votes"] += 1
        store.save(notes)
        # Update the user object
        user_store = UserStore()
        users = user_store.get()
        user_id = None
        for id, user in enumerate(users):
            if user['name'] == request.session.get("user_name"):
                user_id = id
        # user_id = [id for id, user in enumerate(users)
        #            if user["name"] == request.session.get("user_name")].pop(0)
        if user_id is not None:
            users[user_id]["voted_notes"].append(note_id)
            user_store.save(users)
            # Update the session
            request.session["user_votes"] = users[user_id]["voted_notes"]
            return redirect(reverse("notes:details", args=[note_id]))
        else:
            return redirect(reverse("notes:home"))
            

