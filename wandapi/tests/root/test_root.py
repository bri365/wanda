
from wandapi.tests import utils
import falcon
from testfixtures import log_capture


class TestRootController(utils.FunctionalTest):
    """Root resource tests."""

    layer = utils.TopLayer

    # noinspection PyUnusedLocal
    @log_capture()
    def test_options(self, log):
        response = self.simulate_options('/api/versions', headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_OK)

    # noinspection PyUnusedLocal
    @log_capture()
    def test_accept_json(self, log):
        response = self.simulate_get('/api/versions', headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_OK)

    # noinspection PyUnusedLocal
    @log_capture()
    def test_star_request_accept(self, log):
        response = self.simulate_get('/api/versions', headers={'Accept': '*/*'})
        self.assertEqual(response.status, falcon.HTTP_OK)

    @log_capture()
    def test_empty_request_body(self, log):
        response = self.simulate_post('/api/bogus',
                                      headers={'Accept': 'application/json',
                                               'Content-Type': 'application/json',
                                               'Content-Length': '8'})
        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(response.json['result'], 'Empty request body - valid JSON required')
        self.assertIn('time', response.json)
        self.assertIn('POST:/api/bogus:400 Bad Request:Empty request body - valid JSON required',
                      str(log))

    @log_capture()
    def test_method_not_allowed(self, log):
        response = self.simulate_delete('/api/versions', headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_METHOD_NOT_ALLOWED)
        self.assertEqual(response.json['result'], "['GET', 'OPTIONS']")
        self.assertIn('DELETE:/versions:405 Method Not Allowed', str(log))

    @log_capture()
    def test_non_json_request_accept(self, log):
        response = self.simulate_get('/api/versions', headers={'Accept': 'text/html'})
        self.assertEqual(response.status, falcon.HTTP_NOT_ACCEPTABLE)
        self.assertEqual(response.json['result'],
                         'WandAPI only supports JSON encoded responses')
        self.assertIn('GET:/api/versions:406 Not Acceptable', str(log))

    @log_capture()
    def test_non_json_request_content(self, log):
        response = self.simulate_post('/api/bogus', body='non json content',
                                      headers={'Accept': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(response.json['result'],
                         'WandAPI only supports JSON encoded requests')
        self.assertIn('POST:/api/bogus:415 Unsupported Media Type', str(log))

    @log_capture()
    def test_non_json_request_content_bad_content_type(self, log):
        response = self.simulate_post('/api/bogus', body='non json content',
                                      headers={'Accept': 'application/json',
                                               'Content-Type': 'application/warez'})
        self.assertEqual(response.status, falcon.HTTP_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(response.json['result'],
                         'WandAPI only supports JSON encoded requests')
        self.assertIn('POST:/api/bogus:415 Unsupported Media Type', str(log))

    @log_capture()
    def test_post_request_empty_body(self, log):
        response = self.simulate_post('/api/bogus', body='',
                                      headers={'Accept': 'application/json',
                                               'Content-Type': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(response.json['result'], 'Empty request body - valid JSON required')
        self.assertIn('time', response.json)
        self.assertIn('POST:/api/bogus:400 Bad Request:Empty request body - valid JSON required',
                      str(log))

    @log_capture()
    def test_put_request_empty_body(self, log):
        response = self.simulate_post('/api/bogus', body='',
                                      headers={'Accept': 'application/json',
                                               'Content-Type': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(response.json['result'], 'Empty request body - valid JSON required')
        self.assertIn('time', response.json)
        self.assertIn('POST:/api/bogus:400 Bad Request:Empty request body - valid JSON required',
                      str(log))

    @log_capture()
    def test_non_json_request_data(self, log):
        response = self.simulate_post('/api/bogus', body='non json',
                                      headers={'Accept': 'application/json',
                                               'Content-Type': 'application/json'})
        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)
        self.assertEqual(
            response.json['result'],
            'Could not decode request body - JSON was incorrect or not encoded as UTF-8')
        self.assertIn('mS', response.json['time'])
        self.assertIn('POST:/api/bogus:400 Bad Request', str(log))
