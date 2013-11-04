from functools import partial
from .macro4 import MacroFor
from flask import url_for


class UlMacro(MacroFor):
    """A generalized list (of links or independent macros)

    :param list_items: a list of LiItems items
    :param css_class:  ul class
    :param css_id:     ul id
    """
    def __init__(self, list_items, **kwargs):
        self.list_items = list_items
        self.css_class = kwargs.get('css_class', None)
        self.css_id = kwargs.get('css_id', None)
        super(UlMacro, self).__init__(mname='ullinks',
                                      mwhere="macros/list.html")


class LiItem(MacroFor):
    """A list item containing a link. Any kwargs left over will be passed to
    url creation

    :param name:         visible string printed as the link
    :param for_url:      the flask route passed to url_for
    :param css_class:    the li css class, default
    :param independent:  set True if item is another Macro, defaults to False
    """
    def __init__(self, name, for_url=None, **kwargs):
        self.name = name
        self.css_class = kwargs.pop('css_class', None)
        self.independent = kwargs.pop('independent', False)
        self.route = for_url
        self.route_add = kwargs
        self.url = partial(self.generate_url)
        super(LiItem, self).__init__(mname="lilink",
                                     mwhere="macros/list.html")

    def generate_url(self):
        return url_for(self.route, **self.route_add)


class AccordianItem(object):
    def __init__(self,
                 group_label,
                 interior,
                 is_open=True,
                 display_label=None):
        self.group_label = group_label
        self.interior = interior
        self.is_open = is_open
        self.of_accordian = None
        self.display_label = display_label

    @property
    def label(self):
        if self.display_label:
            return self.display_label
        else:
            return self.group_label


class AccordianGroupMacro(MacroFor):
    def __init__(self,
                 tag,
                 accordian_label,
                 accordian_groups,
                 group_class="accordian-macro"):
        self.accordian_groups = accordian_groups
        self.accordian_label = accordian_label
        for g in accordian_groups:
            g.of_accordian = accordian_label
        self.accordian_groups = accordian_groups
        self.group_class = group_class
        super(AccordianGroupMacro, self).__init__(tag=tag,
                                                  mwhere="macros/accordian.html",
                                                  mname="accordian_group_macro")


class BreadCrumbItem(object):
    def __init__(self, requested_label, route, active=False):
        self._label = requested_label
        self.route = None
        self.route_params = None
        self.active = active
        self.parse_route(route)

    @property
    def default_label(self):
        return str(self._label)

    @property
    def label(self):
        return getattr(self, self._label, self.default_label)

    def parse_route(self, route):
        if isinstance(route, dict):
            self.route = route.pop('base')
            self.route_params = route
        else:
            self.route = route

    @property
    def generate_url(self):
        if self.route_params:
            return url_for(self.route, **self.route_params)
        else:
            return url_for(self.route)


class BreadCrumbMacro(MacroFor):
    def __init__(self, tag, items, css_id=None, css_class=None, span_item="/"):
        self.items = items
        self.css_id = css_id
        self.css_class = css_class
        self.span_item = span_item
        super(BreadCrumbMacro, self).__init__(tag=tag,
                                              mwhere="macros/breadcrumb.html",
                                              mname = "breadcrumbs_macro")


class TabItem(object):
    def __init__(self, label, tab_label, **kwargs):
        self.label = label
        self.tab_label = tab_label
        self.set_tab(kwargs)

    def set_tab(self, kwargs):
        if kwargs:
            for k,v in kwargs.items():
                if k in ('minimal', 'external', 'static', 'independent', 'content'):
                    tab_type = k
                    tab_content = v
                else:
                    tab_type = 'content'
                    tab_content = "None"
                setattr(self, 'kind', tab_type)
                setattr(self, '_li', getattr(self, "make_li", None)(tab_type))
                setattr(self, tab_type, tab_content)

    def make_li(self, tab_type):
        tab = "{}_li".format(tab_type)
        return MacroFor(mwhere="macros/tabs.html",
                        mname=tab).renderable


class TabGroupMacro(MacroFor):
    def __init__(self, **kwargs):
        self.tag = kwargs.get('tag', None)
        self.minimal = kwargs.get('minimal', False)
        if self.minimal:
            self.mname = "minimal_tabs"
        else:
            self.mname = "bootstrap_tabs"
        self.mwhere = kwargs.get('mwhere', "macros/tab.html")
        self.tabs_label = kwargs.get('tabs_label', None)
        self.tab_groups = kwargs.get('tab_groups', None)
        self.tabs_nav_class = kwargs.get('tabs_nav_class',"tabbed-nav")
        self.tabs_content_class = kwargs.get('tabs_content_class', "content-for-tabs")
        super(TabGroupMacro, self).__init__(tag=self.tag,
                                            mname=self.mname,
                                            mwhere=self.mwhere,
                                            mattr={'tabs_label': self.tabs_label,
                                                   'tab_groups': self.tab_groups,
                                                   'tabs_nav_class': self.tabs_nav_class,
                                                   'tabs_content_class': self.tabs_content_class})
