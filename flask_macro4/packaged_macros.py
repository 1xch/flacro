from .macro4 import MacroFor
from flask import url_for

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
                                                  mwhere="macros/accordians.html",
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
                                              mwhere="macros/breadcrumbs.html",
                                              mname = "breadcrumbs_macro")


class TabItem(object):
    def __init__(self, label, tab_label, **kwargs):
        self.label = label
        self.tab_label = tab_label
        self.set_tab(kwargs)

    def set_tab(self, kwargs):
        if kwargs:
            for k,v in kwargs.items():
                if k in ('external', 'static', 'independent', 'content'):
                    tab_item = k
                    tab_content = v
                else:
                    tab_item = 'content'
                    tab_content = "None"
                setattr(self, '_li', getattr(self, "make_li", None)(tab_item))
                setattr(self, tab_item, tab_content)

    def make_li(self, kind_of):
        tab_item = "{}_li".format(kind_of)
        return MacroFor(mwhere="macros/tabs.html",
                        mname=tab_item).renderable


class TabGroupMacro(MacroFor):
    def __init__(self, **kwargs):
        super(TabGroupMacro, self).__init__(tag=kwargs.get('tag', None),
                                            mwhere="macros/tabs.html",
                                            mname="tabs_macro",
                                            mattr={'tabs_label': kwargs.get('tabs_label', None),
                                                   'tab_groups': kwargs.get('tab_groups', None),
                                                   'tabs_nav_class': kwargs.get('tabs_nav_class',"tabbed-nav"),
                                                   'tabs_content_class': kwargs.get('tabs_content_class', "content-for-tabs")})
