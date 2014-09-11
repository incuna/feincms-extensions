from django.template import TemplateSyntaxError
from django.test import TestCase
import mock

from ..templatetags.feincms_menu import do_feincms_page_menu


class TestFeinCMSPageMenu(TestCase):
    def test_no_argument(self):
        parser = mock.Mock()
        token = mock.Mock()

        # first argument is the template tag
        token.split_contents.return_value = ['feincms_page_menu']

        with self.assertRaises(TemplateSyntaxError):
            do_feincms_page_menu(parser, token)
