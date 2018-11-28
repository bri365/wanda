
import json
import os

from wandapi.api import setup_app
from wandapi.tests import config
import falcon
from falcon import testing


setup_app(config)

# frequently used test case inputs
EMPTY_OR_WHITESPACE_STRINGS = ['', ' ', '    ', '        ']


class TestResponse(object):
    """Object intended to look like an instance of falcon.testing.client.Result."""

    json = None
    status = None


class FunctionalTest(testing.TestCase):
    """Functional test base class for integration testing."""

    schema_version = None
    schema_definition = None

    def setUp(self):
        super(FunctionalTest, self).setUp()
        self.app = setup_app(config)
        self.maxDiff = None

    def tearDown(self):
        pass

    @staticmethod
    def _headers():
        return {'Accept': 'application/json',
                'content_type': 'application/json'}

    # helper methods
    def _delete(self, path, params=None):
        # if you've come here to add support for request bodies in an HTTP DELETE operation,
        # stop now, as many clients (e.g. Android) do not support this, and it's just awkward
        # with respect to RFC2616.
        return self.simulate_delete(
            '/api/v1/{}'.format(path), params=params,
            headers={'Accept': 'application/json'})

    def _get(self, path, params=None):
        return self.simulate_get(
            '/api/v1/{}'.format(path), params=params,
            headers={'Accept': 'application/json'})

    def _patch(self, path, data, params=None):
        return self.simulate_patch(
            '/api/v1/{}'.format(path), body=json.dumps(data), params=params,
            headers={'Accept': 'application/json',
                     'content_type': 'application/json'})

    def _post(self, path, data, params=None, content_type='application/json'):
        headers = {'Accept': 'application/json',
                   'content_type': content_type}
        body = json.dumps(data) if content_type == 'application/json' else data
        return self.simulate_post(
            '/api/v1/{}'.format(path), body=body, params=params, headers=headers)

    def _put(self, path, data, params=None, content_type=None):
        if content_type is None:
            # Default is JSON.
            content_type = 'application/json'
            body = json.dumps(data)
        else:
            # Assume the caller formatted data as needed for the content type.
            body = data
        return self.simulate_put(
            '/api/v1/{}'.format(path), body=body, params=params,
            headers={'Accept': 'application/json',
                     'content_type': content_type})

    @staticmethod
    def _convert_requests_response(response):
        """Convert a response from the 'requests' module to one compatible with falcon testing.

        Arguments:
            response (requests.models.Response): the response object from 'requests'

        Returns:
            TestResponse: object with 'status' and 'json' properties suitable for use with
                convenience assertions within this class.
        """
        test_response = TestResponse()
        test_response.json = response.json()
        status_var = 'HTTP_{}'.format(response.status_code)
        test_response.status = getattr(falcon, status_var)
        return test_response

    @staticmethod
    def cleanup_file(filename):
        """Delete specified file.

        Arguments:
            filename (str): The file to delete.
        """
        if os.path.isfile(filename):
            os.remove(filename)

    @staticmethod
    def _json_roundtrip(obj):
        """Roundtrip object through JSON.

        This converts string values into unicode so that diffs are more legible.
        """
        return json.loads(json.dumps(obj, sort_keys=True))

    def assertJsonDictEqual(self, response, reference):  # noqa: N802
        """Assert that dicts are equal after coercing into JSON.

        This gets rid of the diffs on `u'` everywhere.
        """
        self.assertDictEqual(self._json_roundtrip(response), self._json_roundtrip(reference))

    def assertResponseStatusOk(self, response):  # noqa: N802
        """Assert that the response status is HTTP 'OK'."""
        self.assertEqual(response.status, falcon.HTTP_OK)


class TopLayer(object):
    """Top layer class for nose2 fixture layers."""

    pass
