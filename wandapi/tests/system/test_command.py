
from unittest import TestCase

from wandapi.command import api
from mock import patch
from testfixtures import log_capture


class TestCommand(TestCase):
    """Command tests."""

    @log_capture()
    def test_api_server(self, log):
        mock_wsgi = patch('wandapi.command.api.wsgi').start()
        mock_listen = patch('wandapi.command.api.listen').start()
        api.run_server()
        self.assertTrue(mock_listen.called)
        self.assertTrue(mock_wsgi.server.called)
        self.assertIn('INFO\n  API Initialized', str(log))
