
from wandapi.resources.base import BaseResource


class WandCollection(BaseResource):
    """REST resource controller for hosts."""

    # noinspection PyUnusedLocal
    @staticmethod
    def on_get(req, resp):
        """Return a list of wands."""
        req.context['result'] = []


class WandItem(BaseResource):
    """REST resource controller for individual host objects."""

    # noinspection PyUnusedLocal
    @staticmethod
    def on_get(req, resp, uuid=None):
        """Return the wand with the given uuid."""
        pass
