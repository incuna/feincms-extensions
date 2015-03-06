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
