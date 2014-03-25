from __future__ import with_statement

import sys
import os
from flask import Flask, render_template, current_app

from tests import *


class FlacroBaseCase(FlacroTest):
    def test_bases(self): pass

    def test_macro_static(self):
        rv = self.app.test_client().get('/static_macro')
        self.assertIn(b'STATIC MACRO', rv.data)

    def test_macro_content(self):
        rv = self.app.test_client().get('/content_macro')
        self.assertIn(b'THING', rv.data)

    def test_macro_attr(self):
        rv = self.app.test_client().get('/attr_macro')
        self.assertIn(b'abc', rv.data)

    def test_macro_named(self):
        rv = self.app.test_client().get('/named_macro')
        self.assertIn(b'A NAMED MACRO RENDERED BY NAME', rv.data)
        self.assertIn(b'123', rv.data)


class PackagedMacrosTestCase(FlacroTest):
    def test_list(self):
        rv = self.app.test_client().get('/links_list')
        self.assertIn(b'l1', rv.data)
        self.assertIn(b'href="/one"', rv.data)
        self.assertIn(b'arbitrary=for_attr_macro_route', rv.data)
        self.assertIn(b'a plain item', rv.data)

    def test_accordian(self):
        rv = self.app.test_client().get('/accordian_macro')
        self.assertIn(b'accordian_test-accordion', rv.data)
        self.assertIn(b'#accordian_test', rv.data)

    def test_tabs(self):
        rv = self.app.test_client().get('/tabs_macro')
        self.assertIn(b'tabset-macro', rv.data)
        self.assertIn(b'tab-content', rv.data)
        rv = self.app.test_client().get('minimal_tabs_macro')
        self.assertIn(b'tabset', rv.data)
        self.assertIn(b'minimal', rv.data)


if __name__ == '__main__':
    unittest.main()
