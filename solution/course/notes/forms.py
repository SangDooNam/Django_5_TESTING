"""Forms for the notes app."""

from django import forms

SECTIONS = (
    (None, "-- Any --"),
    ("Web Frameworks", "Web Frameworks"),
    ("Setting up Django", "Setting up Django"),
    ("URL Mapping", "URL Mapping"),
)


class SearchForm(forms.Form):
    """A simple search form."""

    term_of_search = forms.CharField()
    section = forms.ChoiceField(choices=SECTIONS, required=False)


class AddNoteForm(forms.Form):
    """A form to add new notes."""

    section = forms.ChoiceField(choices=SECTIONS)
    text = forms.CharField(widget=forms.Textarea())


class EditNoteForm(forms.Form):
    """A form to edit note texts."""

    section = forms.ChoiceField(choices=SECTIONS, disabled=True)
    text = forms.CharField(widget=forms.Textarea())
