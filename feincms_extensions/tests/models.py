from feincms.models import create_base_model
from feincms.module.page.models import Page

from .content import TestContent


class Dummy(create_base_model()):
    """A fake class for holding content"""


Dummy.register_regions(('body', 'Main'))
Dummy.create_content_type(TestContent)
Dummy.register_extensions(
    'feincms_extensions.render_regions',
)

Page.register_templates({
    'key': 'key',
    'title': 'Title',
    'path': 'base.html',
    'regions': (
        ('body', 'Main'),
    ),
})
Page.register_extensions(
    'feincms_extensions.prepared_date',
)
