
class Version(object):
    """REST resource handler for api and software versions."""

    CURRENT = '1.0'
    SUPPORTED = ['1.0']

    # version format to use in resource path after 'v' (e.g. version 1.0 becomes '/v1/...' in
    # api.py router setup
    PATH = ['1']

    # noinspection PyUnusedLocal
    @staticmethod
    def on_get(req, resp):
        """Return current and supported API versions."""
        req.context['result'] = {'current': Version.CURRENT, 'supported': Version.SUPPORTED}
