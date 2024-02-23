"""Common views of the website."""
from django.views.generic.edit import FormView
from django.views.generic import View
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.shortcuts import redirect

from common.forms import LoginForm
from common.models import UserStore


store = UserStore()
users = store.get()


class LogoutView(View):
    """Log out the user."""

    def get(self, request):
        """Log out and redirect."""
        request.session.flush()
        return redirect("home")


class LoginView(FormView):
    """Form view for the user log in feature."""

    template_name = "common/login.html"
    form_class = LoginForm
    success_url = "/login/"

    def get(self, request):
        """Test."""
        if request.session.get("user_name", None):
            return redirect("home")
        return super().get(request)

    def form_valid(self, form):
        """Check the credentials."""
        user_name = form.data.get("user_name")
        password = form.data.get("password")
        for user in users:
            if user["name"] == user_name and check_password(password, user["password"]):
                self.request.session["user_name"] = user_name
                self.request.session["user_votes"] = user["voted_notes"]
                self.request.session["user_can_write_notes"] = user["role"] in ("admin", "editor")
                break
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user to the home if the authentication worked."""
        if self.request.session.get("user_name", None):
            return reverse("home")
        return super().get_success_url()
