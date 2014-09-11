from django import template
from django.template import TemplateSyntaxError


register = template.Library()


class FeincmsPageMenuNode(template.Node):
    def __init__(self, feincms_page):
        pass


def do_feincms_page_menu(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        message = '{} requires at least one argument (a feincms_page)'.format(bits[0])
        raise TemplateSyntaxError(message)

    kwargs = {}
    args = []
    try:
        for bit in bits[1:]:
            try:
                pair = bit.split('=')
                kwargs[str(pair[0])] = parser.compile_filter(pair[1])
            except IndexError:
                args.append(parser.compile_filter(bit))
    except TypeError:
        raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % bits[0])

    return FeincmsPageMenuNode(*args, **kwargs)

register.tag('feincms_page_menu', do_feincms_page_menu)
