from django.test import TestCase

from .models import Dummy
from .. import content_types


class TestJsonRichTextContent(TestCase):
    model = Dummy.content_type_for(content_types.JsonRichTextContent)

    def test_json(self):
        """A JsonRichTextContent can be rendered to json."""
        text = 'Rich Text'
        content = self.model(region='body', text=text)
        self.assertEqual(content.json(), {'html': text})


class TestJsonSectionContent(TestCase):
    model = Dummy.content_type_for(content_types.JsonSectionContent)

    def test_json(self):
        """A JsonSectionContent can be rendered to json."""
        title = 'Section 1'
        richtext = 'Rich Text'
        content = self.model(region='body', title=title, richtext=richtext)
        self.assertEqual(content.json(), {'title': title, 'html': richtext})
