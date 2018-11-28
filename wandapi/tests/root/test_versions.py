
from wandapi import defines
from wandapi.tests import utils
import falcon
from testfixtures import log_capture


class TestVersions(utils.FunctionalTest):
    """Version resource tests."""

    layer = utils.TopLayer

    # noinspection PyUnusedLocal
    @log_capture()
    def test_path_version_long_ok(self, log):
        response = self.simulate_get('/api/v1.0/wands',
                                     headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_OK)

    # noinspection PyUnusedLocal
    @log_capture()
    def test_path_version_short_ok(self, log):
        response = self.simulate_get('/api/v1/wands',
                                     headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_OK)

    # noinspection PyUnusedLocal
    @log_capture()
    def test_resource_not_found(self, log):
        response = self.simulate_get('/api/v1.0/bogus/url',
                                     headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_NOT_FOUND)
        self.assertEqual(response.json['result'], '')

    # noinspection PyUnusedLocal
    @log_capture()
    def test_version_not_found(self, log):
        response = self.simulate_get('/api/bogus/url',
                                     headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_NOT_FOUND)
        self.assertEqual(response.json['result'], defines.ERROR_API_VERSION_NOT_FOUND)

    # noinspection PyUnusedLocal
    @log_capture()
    def test_version_not_supported(self, log):
        response = self.simulate_get('/api/v99.1001/url',
                                     headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_NOT_FOUND)
        self.assertEqual(response.json['result'], defines.ERROR_API_VERSION_UNSUPPORTED)

    # noinspection PyUnusedLocal
    @log_capture()
    def test_version_ok(self, log):
        response = self.simulate_get('/api/versions', headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_OK)
        expected = {'current': '1.0', 'supported': ['1.0']}
        self.assertDictEqual(response.json['result'], expected)
        self.assertIn('mS', response.json['time'])
