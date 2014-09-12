from django.template import Template, TemplateSyntaxError
from django.test import TestCase
import mock

from ..templatetags.feincms_menu import do_feincms_page_menu


class TestFeinCMSPageMenu(TestCase):
    def setUp(self):
        self.parser = mock.Mock()
        self.token = mock.Mock()

    def test_template_is_registered(self):
        template = Template('{% load feincms_menu %}')
        content = template.render(mock.Mock())
        self.assertEqual(content, '')

    def test_no_argument(self):
        # first argument is the template tag
        self.token.split_contents.return_value = ['feincms_page_menu']

        with self.assertRaises(TemplateSyntaxError):
            do_feincms_page_menu(self.parser, self.token)

    @mock.patch('feincms_extensions.templatetags.feincms_menu.FeincmsPageMenuNode')
    def test_with_feincms_page(self, FeincmsPageMenuNode):
        self.token.split_contents.return_value = ['feincms_page_menu', 'feincms_page']

        do_feincms_page_menu(self.parser, self.token)
        FeincmsPageMenuNode.assert_called_once_with(self.parser.compile_filter())

    def test_with_too_many_arguments(self):
        # first argument is the template tag
        self.token.split_contents.return_value = [
            'feincms_page_menu',
            'feincms_page',
            '',
            '1',
            '1',
            'False',
            'False',
            '',
            'True',
            'extra',
        ]

        with self.assertRaises(TemplateSyntaxError):
            do_feincms_page_menu(self.parser, self.token)
