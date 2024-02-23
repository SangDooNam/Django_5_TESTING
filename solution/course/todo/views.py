"""Todo views."""
from django.views.generic.edit import FormView

from common.forms import LoginForm
from todo.models import todos


class TodoDetails(FormView):
    """Todo details."""

    template_name = "todo/details.html"
    form_class = LoginForm
    # Even if we override the form_valid response, the FormView requires
    # a success_url.
    success_url = "/nothing/"

    def get_context_data(self, *args, **kwargs):
        """Get the notes in the context."""
        context = super().get_context_data()
        context["id"] = self.kwargs["todo_id"]
        if self.request.session.get("user_name", None):
            context["todo"] = todos[self.kwargs["todo_id"] - 1]
            context["num_todos"] = len(todos)
        return context

    def form_valid(self, *args, **kwargs):
        """Override the default redirect behaviour."""
        return self.get(*args, **kwargs)
