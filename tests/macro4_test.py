from __future__ import with_statement

import sys
import os
from collections import OrderedDict
from flask import Flask, render_template, current_app
from flask.ext.macro4 import *

from tests import Macro4Test

class Macro4TestCase(Macro4Test):

    def test_macrofor(self):
        @self.app.route('/')
        def test_page():
            m = MacroFor(mwhere='test_macros/test.html',
                         mname='test_macro_static')
            return render_template('index.html', rstat=m)
        rv = self.app.test_client().get('/')
        self.assertIsNotNone(rv)

    def test_macrofor_value(self):
        @self.app.route('/')
        def test_page():
            m = MacroFor(mwhere='test_macros/test.html',
                         mname='test_macro_with_value')
            return render_template('index.html',
                                   rcont = m,
                                   content="anything")
        rv = self.app.test_client().get('/')
        self.assertIsNotNone(rv)

    def test_macrofor_subclass(self):
        class TestSubclass(MacroFor):
            def __init__(self, anything):
                self.anything=anything
                super(TestSubclass,
                      self).__init__(mwhere='test_macros/test.html',
                                     mname='test_macro_with_value')
        @self.app.route('/')
        def test_page():
            m = TestSubclass("abc")
            return render_template('index.html', m = m)
        rv = self.app.test_client().get('/')
        self.assertIsNotNone(rv)

    def test_tabs(self):
        @self.app.route('/')
        def test_page():
            ti = OrderedDict()
            ti['e'] = TabItem('e', 'E',
                              external="http://somewhere.com")
            ti['s'] = TabItem('s', 'S',
                              static=MacroFor(mwhere='test_macros/test.html',
                                              mname='test_macro_static'))
            ti['i'] = TabItem('i', 'I',
                              independent=MacroFor(mwhere='test_macros/test.html',
                                                   mname='test_macro_with_value'))
            ti['c'] = TabItem('c', 'C',
                              content=MacroFor(mwhere='test_macros/test.html',
                                               mname='test_macro_with_value'))
            tg = TabGroupMacro("test_tabs", ti)
            return render_template('index.html', m = tg)
        rv = self.app.test_client().get('/')
        self.assertIsNotNone(rv)

    def test_accordian(self):
        @self.app.route('/')
        def test_page():
            ai = []
            for i in range(5):
                ai.append(AccordianItem("accordian{}".format(i), i))
            a = AccordianGroupMacro("accordian_test", ai)
            return render_template('index.html', m = a)
        rv = self.app.test_client().get('/')
        self.assertIsNotNone(rv)

    def test_breadcrumb(self):
        @self.app.route('/one')
        def test_page_one():
            return "ONE"
        @self.app.route('/two')
        def test_page_two():
            return "TWO"
        @self.app.route("/")
        def test_page():
            bdi = [BreadCrumbItem('Home', 'test_page_one'),
                   BreadCrumbItem('Profile', 'test_page_two', active=True)]
            m = BreadCrumbMacro(bdi)
            return render_template("index.html", m=m)
        rv = self.app.test_client().get('/')
        self.assertIsNotNone(rv)

if __name__ == '__main__':
    unittest.main()
