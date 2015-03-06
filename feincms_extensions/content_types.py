from feincms.content.richtext.models import RichTextContent


class JsonRichTextContent(RichTextContent):
    class Meta(RichTextContent.Meta):
        abstract = True

    def json(self, **kwargs):
        """Return a json serializable dictionary containing the content."""
        return {'html': self.text}
