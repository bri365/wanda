
from wandapi.tests import utils
import falcon
from testfixtures import log_capture


# noinspection PyUnusedLocal
class TestWands(utils.FunctionalTest):
    """Wand resource tests."""

    layer = utils.TopLayer

    def setUp(self):
        """Set up."""
        super(TestWands, self).setUp()

    # list wands
    @log_capture()
    def test_list_wands_zero(self, log):
        response = self._get('wands')
        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertEqual(len(response.json['result']), 0)
