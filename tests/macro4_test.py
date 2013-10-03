from __future__ import with_statement

import sys
import os
from flask import Flask, render_template, current_app
from flask_macro4 import *

from tests import *

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


class PackagedMacrosTestCase(Macro4Test):
    def test_tabs(self):
        rv = self.app.test_client().get('/tabs_macro')
        self.assertIn(b'<li><a href="http://somewhere.com">E</a></li>', rv.data)
        self.assertIn(b'STATIC MACRO', rv.data)
        self.assertIn(b'independent', rv.data)
        self.assertIn(b'<a href="#c" data-toggle="tab">C</a>', rv.data)
        self.assertIn(b'content', rv.data)

    def test_accordian(self):
        rv = self.app.test_client().get('/accordian_macro')
        self.assertIn(b'<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordian_test" href="#collapseAccordian3">', rv.data)
        self.assertIn(b'<div id="collapseAccordian3" class="accordion-body collapse in">', rv.data)

    def test_breadcrumb(self):
        rv = self.app.test_client().get('/breadcrumbs_macro')
        self.assertIn(b'<li class="active"><a href="/two">Profile</a></li>', rv.data)

if __name__ == '__main__':
    unittest.main()
