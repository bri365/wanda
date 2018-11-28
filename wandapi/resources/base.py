
import logging


class BaseResource(object):
    """Provides common attributes/methods for API resources."""

    def __init__(self):
        """Initialize logging."""
        self._logger = logging.getLogger('wandapi')
        self.count = None
        self.data = None
        self.req = None
        self.resp = None

    def set_result(self):
        """Set properties of the Falcon req.context object."""
        self.req.context['count'] = self.count
        self.req.context['result'] = self.data
