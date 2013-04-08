from __future__ import with_statement

import sys
import os
from collections import OrderedDict
from flask import Flask, render_template
from flask.ext.macro4 import *

import unittest

class Macro4TestCase(unittest.TestCase):

    def _set_app_config(self, app):
        pass

    def setUp(self):
        app = Flask(__name__)
        #app.debug = True
        app.config['TESTING'] = True
        self._set_app_config(app)
        Macro4().init_app(app)
        self.app = app

    def tearDown(self):
        self.app = None

    def test_00_macrofor(self):
        @self.app.route('/')
        def test_page():
            m = MacroFor(macro='test.html', macro_var='test_macro_static', macro_attr={'static': True})
            return render_template('test_page.html', m = m)
        self.app.test_client().get('/')

    def test_00a_macrofor_value(self):
        @self.app.route('/')
        def test_page():
            m = MacroFor(macro='test.html', macro_var='test_macro_with_value', macro_attr={'static': False})
            return render_template('test_page.html', m = m)
        self.app.test_client().get('/')

    def test_00b_macrofor_subclass(self):
        class TestSubclass(MacroFor):
            def __init__(self, anything):
                self.anything=anything
                self.static = False
                super(TestSubclass, self).__init__(macro='test.html', macro_var='test_macro_with_value')
        @self.app.route('/')
        def test_page():
            m = TestSubclass("abc")
            return render_template('test_page.html', m = m)
        self.app.test_client().get('/')

    def test_01_tabs(self):
        @self.app.route('/')
        def test_page():
            ti = OrderedDict()
            ti['e'] = TabItem('e', 'E', external="http://somewhere.com")
            ti['s'] = TabItem('s', 'S', static=MacroFor(macro='test.html', macro_var='test_macro_static'))
            ti['i'] = TabItem('i', 'I', independent=MacroFor(macro='test.html', macro_var='test_macro_with_value'))
            ti['c'] = TabItem('c', 'C', content=MacroFor(macro='test.html', macro_var='test_macro_with_value'))
            tg = TabGroupMacro("test_tabs", ti)
            return render_template('test_page.html', m = tg)
        self.app.test_client().get('/')

    def test_02_accordian(self):
        @self.app.route('/')
        def test_page():
            ai = []
            for i in range(5):
                ai.append(AccordianItem("accordian{}".format(i), i))
            a = AccordianGroupMacro("accordian_test", ai)
            return render_template('test_page.html', m = a)
        self.app.test_client().get('/')

    def test_03_breadcrumb(self):
        pass


if __name__ == '__main__':
    unittest.main()
