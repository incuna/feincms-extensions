from django import template
from django.template import TemplateSyntaxError


register = template.Library()


class FeincmsPageMenuNode(template.Node):
    def __init__(self, feincms_page):
        pass


def do_feincms_page_menu(parser, token):
    # first argument is the template tag
    bits = token.split_contents()

    if len(bits) == 1:
        message = '"{}" requires at least one argument (a feincms_page)'.format(bits[0])
        raise TemplateSyntaxError(message)
    if len(bits) > 9:
        message = '"{}" tag accepts no more than 8 arguments.'.format(bits[0])
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
        message = 'Bad arguments for tag "{}"'.format(bits[0])
        raise template.TemplateSyntaxError(message)

    return FeincmsPageMenuNode(*args, **kwargs)

register.tag('feincms_page_menu', do_feincms_page_menu)
