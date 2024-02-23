"""General file store interface."""
import json
import os

from django.conf import settings

STORE_PATH = os.path.join(settings.BASE_DIR, "data")
try:
    os.mkdir(STORE_PATH)
except FileExistsError:
    pass


class CustomStore:
    """Main store class."""

    def __init__(self):
        """Constructor."""
        self.file_path = os.path.join(STORE_PATH, self.model_name + ".json")

    def get(self):
        """Return the content."""
        content = None
        try:
            with open(self.file_path) as file:
                content = file.read()
        except FileNotFoundError:
            self.save(self.backup)
            return self.backup
        if content:
            return json.loads(content)
        return content

    def save(self, content):
        """Replace the content in the store."""
        if isinstance(content, (list, dict)):
            content = json.dumps(content)
        with open(self.file_path, "w") as file:
            file.write(content)
