from flask import get_template_attribute, url_for, Blueprint
from jinja2 import Template

blueprint = Blueprint('macro4', __name__, template_folder='pages')

class MacroForMeta(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            interface_id = name.lower()
            cls.registry[interface_id] = cls

        super(MacroForMeta, cls).__init__(name, bases, dct)


class MacroFor(object):
    __metaclass__ = MacroForMeta

    def __init__(self, **kwargs):
        self.macro = kwargs.get('macro', None)
        self.macro_var = kwargs.get('macro_var', None)
        self._macro_attr = kwargs.get('macro_attr', None)
        self._macros = kwargs.get('macros', None)
        if self._macro_attr:
            for k,v in self._macro_attr.iteritems():
                setattr(self, k, v)
        if self._macros:
            for k,v in self._macros.iteritems():
                setattr(self, k, self.get_macro(k, macro_attr=v))

    def get_macro(self, macro_var, macro_attr=None):
        return MacroFor(macro=self.macro, macro_var=macro_var, macro_attr=macro_attr)

    @property
    def renderable(self):
        try:
            return get_template_attribute(self.macro, self.macro_var)
        except Exception, e:
            print e

    @property
    def render(self):
        return self.renderable(self)

    def render_with(self, content):
        return self.renderable(content)

    def __repr__(self):
        return "<{}: {}>".format(self.macro, self.macro_var)


class AccordianItem(object):
    def __init__(self, group_label, interior, is_open=True, display_label=None):
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
    def __init__(self, accordian_label, accordian_groups, group_class="accordian-macro"):
        self.accordian_groups = accordian_groups
        self.accordian_label = accordian_label
        for g in accordian_groups:
            g.of_accordian = accordian_label
        self.accordian_groups = accordian_groups
        self.group_class = group_class
        super(AccordianGroupMacro, self).__init__(macro="macros/accordian.html",
                                                  macro_var="accordian_group_macro")


class BreadCrumbItem(object):
    def __init__(self, requested_label, route, active=False):
        self._label = requested_label
        self.route = None
        self.route_params = None
        self.active = active
        self.parse_route(route)

    @property
    def default_label(self):
        return self._label

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
    def __init__(self, items, css_id=None, css_class=None, span_item="/"):
        self.items = items
        self.css_id = css_id
        self.css_class = css_class
        self.span_item = span_item
        super(BreadCrumbMacro, self).__init__(macro="macros/breadcrumbs.html",
                                              macro_var = "breadcrumbs_macro")


class TabItem(object):
    def __init__(self, kind_of, label, tab_label, **kwargs):
        self._li = getattr(self, "make_li", None)(kind_of)
        self.label = label
        self.tab_label = tab_label
        for k,v in kwargs.iteritems():
            if k in ('external', 'static', 'independent', 'content'):
                setattr(self, k, v)

    def make_li(self, kind_of):
        return MacroFor(macro="macros/tabs.html", macro_var="{}_li".format(kind_of)).renderable


class TabGroupMacro(MacroFor):
    def __init__(self, tabs_label,
                       tab_groups,
                       tabs_nav_class="tabbed-nav",
                       tabs_content_class="content-for-tabs"):
        super(TabGroupMacro, self).__init__(macro="macros/tabs.html",
                                            macro_var="tabs_macro",
                                            macro_attr={'tabs_label': tabs_label,
                                                        'tab_groups': tab_groups,
                                                        'tabs_nav_class': tabs_nav_class,
                                                        'tabs_content_class': tabs_content_class})


class Macro4(object):
    """
    flask/jinja2 tools for managing template macros programmtically
    """
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        app.register_blueprint(blueprint)
