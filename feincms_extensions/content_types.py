from feincms.content.richtext.models import RichTextContent
from feincms.content.section.models import SectionContent


class JsonRichTextContent(RichTextContent):
    class Meta(RichTextContent.Meta):
        abstract = True

    def json(self, **kwargs):
        """Return a json serializable dictionary containing the content."""
        return {'html': self.text}


class JsonSectionContent(SectionContent):
    class Meta(SectionContent.Meta):
        abstract = True

    def json(self, **kwargs):
        """Return a json serializable dictionary containing the content."""
        return {'title': self.title, 'html': self.richtext}
