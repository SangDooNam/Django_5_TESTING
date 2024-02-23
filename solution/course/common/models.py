"""Data for the common views"""
from config.store import CustomStore
from django.contrib.auth.hashers import make_password


class UserStore(CustomStore):
    """Store for the users."""

    model_name = "users"
    backup = [
        {
            "name": "admin",
            "password": make_password("admin"),
            "role": "admin",
            "voted_notes": []
        },
        {
            "name": "james",
            "password": make_password("hendrix"),
            "role": "editor",
            "voted_notes": []
        },
        {
            "name": "fred",
            "password": make_password("baggins"),
            "role": "user",
            "voted_notes": []
        },
        {
            "name": "ganesh",
            "password": make_password("the_grey"),
            "role": "user",
            "voted_notes": []
        }
    ]
