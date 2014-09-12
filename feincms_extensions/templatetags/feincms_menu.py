from django import template
from django.template import TemplateSyntaxError
from feincms.module.page.models import Page, PageManager


register = template.Library()


class FeincmsPageMenuNode(template.Node):
    """
    Render the page navigation.
    arguments:
        feincms_page: The current feincms_page.
        css_id: The css (dom) id to be used for the menu. Ignored if `ul_tag` is False.
        level: The level at which to start the navigation.
        depth: The depth of sub navigation to include.
        show_all_subnav: Whether to show all sub navigation items (or just the ones in the current pages branch).
        extended: Whether the navigation has been extended (to enable third party apps to exgtend the navigation).
        ul_tag: Do we wrap the output in a <ul>? If False, `css_id` is ignored.
    example usage:
        {% feincms_page_menu feincms_page depth=2 %}
    """
    def __init__(self,  feincms_page, css_id='', level=1, depth=1, show_all_subnav=False, extended=False, css_class_prefix='', ul_tag=True):
        self.feincms_page = feincms_page
        self.css_id = css_id
        self.css_class_prefix = css_class_prefix
        self.level = level
        self.depth = depth
        self.show_all_subnav = show_all_subnav
        self.extended = extended
        self.ul_tag = ul_tag

    def render(self, context):
        self.render_context = context
        feincms_page = self.feincms_page.resolve(context)

        if not isinstance(feincms_page, Page):
            return ''

        def get_value(tag_arg):
            if isinstance(tag_arg, template.FilterExpression):
                return tag_arg.resolve(context)
            else:
                return tag_arg

        level = int(get_value(self.level))
        depth = int(get_value(self.depth))
        css_id = get_value(self.css_id)
        css_class_prefix = get_value(self.css_class_prefix)
        show_all_subnav = bool(get_value(self.show_all_subnav))
        extended = get_value(self.extended)
        ul_tag = bool(get_value(self.ul_tag))

        if not 'request' in context:
            raise ValueError("No request in the context. Try using RequestContext in the view.")

        request = context['request']

        entries = self.what(feincms_page, level, depth, show_all_subnav, extended)

        if not entries:
            return ''

        def get_next_item(item, remaining, prev_level=-1, extra_context=None):
            context.push()

            if remaining:
                next_level = remaining[0].level
            else:
                next_level = None

            if extra_context:
                context.update(extra_context)

            context['item'] = item
            context['url'] = item.get_absolute_url()
            context['is_current'] = context['url'] == request.path
            context['title'] = item.title

            if 'css_class' in context:
                context['css_class'] += ' ' + css_class_prefix + item.slug
            else:
                context['css_class'] = css_class_prefix + item.slug

            if context['is_current'] or is_equal_or_parent_of(item, feincms_page):
                context['css_class'] += ' selected'
                context['is_current_or_parent'] = True

            if next_level is None:
                context['css_class'] += ' last'
            elif next_level > item.level:
                context['down'] = next_level - item.level
                # look ahead to the next at this level
                for next in remaining:
                    if next.level == item.level:
                        break
                    elif next.level < item.level:
                        context['css_class'] += ' last'
                        break
            elif next_level < item.level:
                context['up'] = item.level - next_level
                context['css_class'] += ' last'

            if prev_level < item.level:
                context['css_class'] += ' first'

            html = template.loader.get_template('incunafein/page/menuitem.html').render(context)
            context.pop()

            return html

        output = ''
        items = list(entries)
        item = items.pop(0)
        prev_level = -1
        while items:
            output += get_next_item(item, items, prev_level)
            prev_level = item.level
            item = items.pop(0)

        output += get_next_item(item, items, prev_level)

        if ul_tag:
            if css_id:
                attrs = ' id="%s"' % css_id
            else:
                attrs = ''
            output = '<ul%s>%s</ul>' % (attrs, output)
        return output

    def what(self, instance, level=1, depth=1, show_all_subnav=False, extended=False):
        mptt_limit = level + depth - 1  # adjust limit to mptt level indexing

        entries = self.entries(instance, level, depth, show_all_subnav)

        if extended:
            _entries = list(entries)
            entries = []

            extended_node_rght = []  # rght value of extended node.
                                     # used to filter out children of
                                     # nodes sporting a navigation extension

            for entry in _entries:
                if (show_all_subnav or entry == instance) and getattr(entry, 'navigation_extension', None):
                    entries.append(entry)
                    extended_node_rght.append(entry.rght)

                    entries.extend(e for e in entry.extended_navigation(depth=depth,
                        request=self.render_context.get('request', None),
                        show_all_subnav=show_all_subnav)
                        if getattr(e, 'level', 0) < mptt_limit)

                else:
                    if extended_node_rght:
                        if entry.rght < extended_node_rght[-1]:
                            continue
                        else:
                            extended_node_rght.pop()

                    entries.append(entry)

        return entries

    def ancestor_siblings(self, instance, level=1):
        opts = instance._meta
        ancestors = instance.get_ancestors().filter(in_navigation=True, level__gte=level - 1)
        return instance._tree_manager.filter(**{'in_navigation': True, '%s__in' % opts.parent_attr: ancestors})

    def entries(self, instance, level=1, depth=1, show_all_subnav=False):
        if level <= 1:
            if depth == 1:
                return Page.objects.toplevel_navigation()
            elif show_all_subnav:
                return Page.objects.in_navigation().filter(level__lt=depth)
            else:
                queryset = Page.objects.toplevel_navigation()
                if instance.level > 1:
                    # Get the ancestors (and their direct children) between
                    # this level and top of tree.
                    queryset = queryset | self.ancestor_siblings(instance)
                queryset = queryset | \
                        instance.get_siblings(include_self=True).filter(in_navigation=True, level__lt=depth) | \
                        instance.children.filter(in_navigation=True, level__lt=depth)
                return PageManager.apply_active_filters(queryset)

        # mptt starts counting at 0, NavigationNode at 1; if we need the submenu
        # of the current page, we have to add 2 to the mptt level
        toplevel = instance
        if toplevel.level + 2 == level:
            pass
        elif instance.level + 2 < level:
            try:
                queryset = instance.get_descendants().filter(level=level - 2, in_navigation=True)
                toplevel = PageManager.apply_active_filters(queryset)[0]
            except IndexError:
                return []
        else:
            toplevel = instance.get_ancestors()[level - 2]

        if depth == 1:
            return toplevel.children.in_navigation()
        elif show_all_subnav:
            queryset = toplevel.get_descendants().filter(level__lte=toplevel.level + depth, in_navigation=True)
            return PageManager.apply_active_filters(queryset)
        else:
            queryset = instance.children.in_navigation() | \
                    self.ancestor_siblings(instance, level=level) | \
                    instance.get_siblings(include_self=True).filter(in_navigation=True, level__gte=level - 1, level__lte=instance.level + depth)
            if toplevel != instance:
                queryset = queryset | toplevel.children.in_navigation()
            return PageManager.apply_active_filters(queryset)


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
