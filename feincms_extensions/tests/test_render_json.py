from django.test import TestCase
from mock import patch, MagicMock

from .factories import DummyFactory


class TestExtension(TestCase):
    def test_json_regions(self):
        request = MagicMock()

        dummy = DummyFactory.create()
        json_path = 'feincms_extensions.tests.content.TestContent.json'
        expected_dict = {'foo': 'bar'}
        with patch(json_path) as json:
            json.return_value = expected_dict
            self.assertEqual(
                dummy.render_json(request),
                {'body': [expected_dict]},
            )

        json.assert_called_once_with(request=request)
