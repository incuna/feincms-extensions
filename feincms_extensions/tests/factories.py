from django.contrib.auth import get_user_model
import factory
from feincms.module.page.models import Page

from . import content, models


User = get_user_model()


class DummyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Dummy

    @factory.post_generation
    def content(self, create, extracted, **kwargs):
        if not create:
            return
        Content = models.Dummy.content_type_for(content.TestContent)
        Content.objects.create(parent=self, region='body')


class PageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Page

    title = factory.Sequence('Page {}'.format)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    email = factory.Sequence('{}@example.com'.format)
