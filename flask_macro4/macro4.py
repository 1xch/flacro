import re
from flask import current_app, Blueprint
from werkzeug import LocalProxy


_macro_for = LocalProxy(lambda: current_app.jinja_env)
_glo = LocalProxy(lambda:  current_app.jinja_env.globals)


ATTR_BLACKLIST = re.compile("mwhere|mname|mattr|macros|^_")


class MacroForMeta(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            interface_id = name.lower()
            cls.registry[interface_id] = cls

        super(MacroForMeta, cls).__init__(name, bases, dct)


class MacroFor(object):
    """
    A container class for managing, holding and returning Jinja2 macros within
    a Flask application. May be instanced as-is or used as a mixin.

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

        :param mwhere: the file location of your macro
        :param mname:  the name of the macro with the macro file
        :param mattr:  a dict of items you might want to access within your
                       macro e.g. {'a': 'AAAAAA', 'b': 'BBBBB'}
        :param macros: a dict of macros within the same file specified
                       above as mwhere in the form {mname: mattr}
                       e.g. {'my_macro_1': {1: 'x', 2: 'y'},
                             'my_macro_2': {'y': 1, 'x': 2}}
    """

    __metaclass__ = MacroForMeta

    def __init__(self, **kwargs):
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

    def __public__(self):
        return [k for k in self.__dict__.keys() if not ATTR_BLACKLIST.search(k)]

    @property
    def public_vars(self):
        return {k: getattr(self, k, None) for k in self.__public__()}

    def get_macro(self, mname, mattr=None, replicate=False):
        """returns another MacroFor instance from the macro of this instance"""
        if replicate:
            mattr=self.public_vars
        return MacroFor(mwhere=self.mwhere,
                        mname=mname,
                        mattr=mattr)

    def get_template_attribute(self, template_name, attribute):
        m = _macro_for.get_or_select_template(template_name,
                                              globals=_glo).module
        return getattr(m, attribute)

    @property
    def renderable(self):
        """
        the macro held but not called
        """
        try:
            return self.get_template_attribute(self.mwhere, self.mname)
        except Exception as e:
            raise e

    @property
    def render(self):
        """
        renders the held macro passing itself as accessible within
        """
        return self.renderable(self)

    @property
    def render_static(self):
        """
        renders the held macro statically, passing in no variable
        """
        return self.renderable()

    def render_with(self, content):
        """
        renders the held macro with the content specified as a parameter(s)
        """
        return self.renderable(content)

    def __repr__(self):
        return "<{}: {}>".format(self.mwhere, self.mname)


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
        app.register_blueprint(self._blueprint)

    @property
    def _blueprint(self):
        return Blueprint('macro4', __name__, template_folder='templates')
