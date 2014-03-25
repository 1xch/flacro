from functools import partial
from .flacro import FlacroFor
from flask import url_for


class LiItem(FlacroFor):
    """A list item containing a link. Any kwargs left over will be passed to
    url creation

    :param li_tag:       a tag for item
    :param kind:         type of li item: plain(tag only), link, macro
    :param li:           is an actual html li, defaults True, set False to eliminate <li></li>
    :param css_class:    a css class
    :param for_url:      the flask route passed to url_for or a url
    :param external:     for_url is external
    """
    def __init__(self, li_tag, **kwargs):
        self.li_tag = li_tag
        self.kind = kwargs.pop('kind', 'plain')
        self.li = kwargs.pop('li', True)
        self.css_class = kwargs.pop('css_class', None)
        self._route = kwargs.pop('for_url', None)
        self._route_external = kwargs.pop('external', False)
        self._route_add = kwargs
        if self._route:
            self.url = partial(self.generate_url, self._route, self._route_add, external=self._route_external)
        super(LiItem, self).__init__(mname="{}item".format(self.kind), mwhere="macros/list.html")

    @staticmethod
    def generate_url(route, route_add, external=False):
        if external:
            return route
        else:
            return url_for(route, **route_add)


class ListMacro(FlacroFor):
    """A generalized list (links, macros, or anything)

    :param list_tag:    a tag for the lsit
    :param kind:        type of list ul or ol
    :param list_items:  a list of LiItems items
    :param css_class:   a css class
    :param css_id:      a css id
    """
    def __init__(self, list_items, **kwargs):
        self.list_tag = kwargs.get('list_tag', None)
        self.kind = kwargs.get('kind', 'ul')
        self.list_items = list_items
        self.css_class = kwargs.get('css_class', None)
        self.css_id = kwargs.get('css_id', None)
        super(ListMacro, self).__init__(mname='listmacro', mwhere="macros/list.html")


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


class AccordianGroupMacro(FlacroFor):
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
        return FlacroFor(mwhere="macros/tab.html",
                        mname=tab).renderable


class TabGroupMacro(FlacroFor):
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
        self.tabset_css_class = kwargs.get('tabset_css_class', "tabset-macro")
        self.vertical = kwargs.get('vertical', False)
        self.justified = kwargs.get('justified', False)
        self.pills =  kwargs.get('pills', False)
        super(TabGroupMacro, self).__init__(tag=self.tag,
                                            mname=self.mname,
                                            mwhere=self.mwhere,
                                            mattr={'tabs_label': self.tabs_label,
                                                   'tab_groups': self.tab_groups,
                                                   'tabs_css_class': self.tabset_css_class,
                                                   'tabs_nav_class': "tabbed-nav-{}".format(self.tabset_css_class),
                                                   'tabs_content_class': "content-for-tabs-{}".format(self.tabset_css_class),
                                                   'vertical': self.vertical,
                                                   'justified': self.justified,
                                                   'pills': self.pills,
                                                   })
