"""ToDo URL Configuration."""
from django.urls import path

from todo.views import TodoDetails

app_name = "todo"
urlpatterns = [
    path('<int:todo_id>/', TodoDetails.as_view(), name="details"),
]
