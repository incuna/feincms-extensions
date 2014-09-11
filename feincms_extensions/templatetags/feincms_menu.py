from django import template
from django.template import TemplateSyntaxError


register = template.Library()


def do_feincms_page_menu(parser, token):
    args = token.split_contents()
    if len(args) < 2:
        message = '{} requires at least one argument (a feincms_page)'.format(args[0])
        raise TemplateSyntaxError(message)

register.tag('feincms_page_menu', do_feincms_page_menu)
