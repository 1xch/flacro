from __future__ import with_statement

import sys
import os
from flask import Flask, render_template, current_app
from flask_macro4 import *

from tests import *
import pprint

class Macro4TestCase(Macro4Test):
    def test_macrofor_static(self):
        rv = self.app.test_client().get('/static_macro')
        self.assertIn(b'STATIC MACRO', rv.data)

    def test_macrofor_content(self):
        rv = self.app.test_client().get('/content_macro')
        self.assertIn(b'THING', rv.data)

    def test_macrofor_attr(self):
        rv = self.app.test_client().get('/attr_macro')
        self.assertIn(b'abc', rv.data)

    def test_macrofor_named(self):
        rv = self.app.test_client().get('/named_macro')
        self.assertIn(b'A NAMED MACRO RENDERED BY NAME', rv.data)
        self.assertIn(b'123', rv.data)


class PackagedMacrosTestCase(Macro4Test):
    def test_accordian(self):
        rv = self.app.test_client().get('/accordian_macro')
        self.assertIn(b'accordian_test-accordion', rv.data)
        self.assertIn(b'#accordian_test', rv.data)

    def test_breadcrumb(self):
        rv = self.app.test_client().get('/breadcrumbs_macro')
        self.assertIn(b'Home', rv.data)
        self.assertIn(b'Profile', rv.data)
        self.assertIn(b'test_breadcrumb', rv.data)

    def test_tabs(self):
        rv = self.app.test_client().get('/tabs_macro')
        self.assertIn(b'test_tabs-tabs', rv.data)
        self.assertIn(b'test_tabs-tabs-content', rv.data)
        rv = self.app.test_client().get('minimal_tabs_macro')
        self.assertIn(b'tabset', rv.data)
        self.assertIn(b'minimal', rv.data)

    def test_links_list(self):
        rv = self.app.test_client().get('/links_list')
        self.assertIn(b'l1', rv.data)
        self.assertIn(b'href="/one"', rv.data)
        self.assertIn(b'arbitrary=for_attr_macro_route', rv.data)


if __name__ == '__main__':
    unittest.main()
