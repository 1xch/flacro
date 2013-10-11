import re
from flask import current_app, Blueprint, _app_ctx_stack
from werkzeug import LocalProxy
from .compat import with_metaclass
from collections import defaultdict
import weakref

_macro4_jinja = LocalProxy(lambda: current_app.jinja_env)
_glo = LocalProxy(lambda:  current_app.jinja_env.globals)


ATTR_BLACKLIST = re.compile("mwhere|mname|mattr|macros|^_")


class MacroForMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = super(MacroForMeta, cls).__new__(cls, name, bases, dct)
        if not hasattr(cls, '_instances'):
            new_class._instances = defaultdict(set)
        return new_class

    def __init__(cls, name, bases, dct):
        if not hasattr(cls, '_registry'):
            cls._registry = {}
        else:
            cls._registry[name.lower()] = cls._instances
        super(MacroForMeta, cls).__init__(name, bases, dct)


class MacroFor(with_metaclass(MacroForMeta)):
    """
    A container class for managing, holding and returning Jinja2 macros within
    a Flask application. Instance as-is or use as a mixin.

    m = MacroFor(mwhere="macros/my_macro.html", mname="my_macro")

    class MyMacro(MacroFor):
        def __init__(self, a, b):
            self.a = a
            self.b = b
            super(MyMacro, self).__init__(mwhere="macros/my_macro.html",
                                          mname="my_macro")

    where "macros/my_macro.html" is a file in your templates directory and
    "my_macro" is a defined macro within that file.

    Takes four keyword arguments.

        :param mwhere: the jinja template file location of your macro
        :param mname:  the name of the macro within the macro file
        :param mattr:  a dict of items you might want to access
                       e.g. {'a': 'AAAAAA', 'b': 'BBBBB'}
        :param macros: a dict of macros within the same file specified
                       above as mwhere in the form {mname: mattr}
                       e.g. {'my_macro_1': {1: 'x', 2: 'y'},
                             'my_macro_2': None}
    """
    def __init__(self, **kwargs):
        self.tag = kwargs.get('tag', None)
        self.mwhere = kwargs.get('mwhere', None)
        self.mname = kwargs.get('mname', None)
        self._mattr = kwargs.get('mattr', None)
        self._macros = kwargs.get('macros', None)
        if self._mattr:
            for k, v in self._mattr.items():
                setattr(self, k, v)
        if self._macros:
            for k, v in self._macros.items():
                setattr(self, k, self.get_macro(k, mattr=v))
        self.register_instance(self)

    @classmethod
    def register_instance(cls, instance):
        if getattr(instance, 'tag', None):
            cls._instances[instance.tag] = instance
        else:
            cls._instances[None].add(instance)

    @property
    def ctx_prc(self):
        def ctx_prc(macro):
            return LocalProxy(lambda: getattr(macro, 'render', None))
        return {self.tag: ctx_prc(self)}

    def _public(self):
        return [k for k in self.__dict__.keys() if not ATTR_BLACKLIST.search(k)]

    @property
    def public(self):
        return {k: getattr(self, k, None) for k in self._public()}

    def update(self, **kwargs):
        [setattr(self, k, v) for k,v in kwargs.items()]

    def get_macro(self, mname, mattr=None, replicate=False):
        """returns another MacroFor instance with a differently named macro from
        the template location of this instance"""
        if replicate:
            mattr=self.public
        return MacroFor(mwhere=self.mwhere,
                        mname=mname,
                        mattr=mattr)

    def jinja_template(self, template_where):
        return _macro4_jinja.get_or_select_template(template_where, globals=_glo).module

    def get_template_attribute(self, template_where, macro_name):
        return getattr(self.jinja_template(template_where), macro_name)

    @property
    def renderable(self):
        """the macro held but not called"""
        try:
            return self.get_template_attribute(self.mwhere, self.mname)
        except RuntimeError:
            return LocalProxy(lambda: self.get_template_attribute(self.mwhere, self.mname))

    @property
    def render(self):
        """calls the macro, passing itself as accessible within"""
        return self.renderable(self)

    @property
    def render_static(self):
        """calls the macro passing in no variable"""
        return self.renderable()

    def render_with(self, content):
        """calls the macro with the content specified as parameter(s)"""
        return self.renderable(content)

    def __repr__(self):
        return "<MacroFor {} ({}: {})>".format(getattr(self, 'tag', None), self.mwhere, self.mname)


class Macro4(object):
    """
    flask/jinja2 tools for managing template macros
    """
    def __init__(self,
                 app=None,
                 register_blueprint=True):
        self.app = app
        self.register_blueprint = register_blueprint
        self.macros = MacroFor._registry

        if self.app is not None:
            self.init_app(self.app)

    def init_app(self, app):
        app.extensions['macro4'] = self
        app.before_request(self.make_ctx_prc)
        if self.register_blueprint:
            app.register_blueprint(self._blueprint)

    def make_ctx_prc(self):
        for mf in self.macros.values():
            for m, macro in mf.items():
                if m:
                    self.app.jinja_env.globals.update(macro.ctx_prc)

    @property
    def _blueprint(self):
        return Blueprint('macro4', __name__, template_folder='templates')
