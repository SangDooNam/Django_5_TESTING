"""Data for the notes views"""
from config.store import CustomStore


class NoteStore(CustomStore):
    """Store for the notes."""

    model_name = "notes"
    backup = [
        {
            "text": "Web frameworks are a way to improve our productivity and make complex things look easy.",
            "section": "Web Frameworks",
            "votes": 0
        },
        {
            "text": "Django is a web framework written with Python that offers a 'batteries included' approach, as opposed to Flask, that aims at minimizing the initial features to reduce the footprint.",
            "section": "Web Frameworks",
            "votes": 0
        },
        {
            "text": "Most web frameworks use the MVC design pattern that states that logic, data and visualization should be kept in different places.",
            "section": "Web Frameworks",
            "votes": 0
        },
        {
            "text": "Setting up Django is very simple. It requires installing Django, starting a project and an app.",
            "section": "Setting up Django",
            "votes": 0
        },
        {
            "text": "The startproject command lets us specify the directory where the project will be created.",
            "section": "Setting up Django",
            "votes": 0
        },
        {
            "text": "Django comes with a development web server that makes it very simple to install and start working.",
            "section": "Setting up Django",
            "votes": 0
        },
        {
            "text": "URL Mapping can be very easy at the beginning but it may become extremely complex in some cases.",
            "section": "URL Mapping",
            "votes": 0
        },
        {
            "text": "URL endpoints may be defined with literals and parameters, which will be passed on to the view.",
            "section": "URL Mapping",
            "votes": 0
        },
        {
            "text": "Parameters passed with the <b><</b> and <b>></b> will be passed as keyword arguments.",
            "section": "URL Mapping",
            "votes": 0
        },
    ]
