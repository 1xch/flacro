from collections import OrderedDict
from unittest import TestCase
from flask import Flask, render_template, current_app
from flask_macro4 import *

class Macro4Test(TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        Macro4(app)
        self.app = app
        static_macro = MacroFor(tag='static_macro', mwhere='test_macros/test.html', mname='test_macro_static')
        content_macro = MacroFor(tag='content_macro', mwhere='test_macros/test.html',mname='test_macro_with_content')
        named_macro = MacroFor(tag='named_macro', mwhere='test_macros/test.html',mname='test_named_macro')

        class TestSubclass(MacroFor):
            def __init__(self, anything, **kwargs):
                self.anything=anything
                super(TestSubclass, self).__init__(tag=kwargs.get('tag', None),
                                                   mwhere='test_macros/test.html',
                                                   mname='test_macro_with_attr')

        attr_macro  = TestSubclass("abc", tag="ATTR_MACRO_1")
        attr_macro_alternate  = TestSubclass("123", tag="ATTR_MACRO_2")

        #accordian macro
        ai = []
        for i in range(5):
            ai.append(AccordianItem("accordian{}".format(i), MacroFor(tag="inner_{}".format(i), mwhere='test_macros/test.html', mname='test_macro_tab_content', mattr={'iam': 'content'})))
        accordian_macro = AccordianGroupMacro("tag_for_accordian_macro", "accordian_test", ai)

        #breadcrumb macro
        bdi = [BreadCrumbItem('Home', 'test_page_one'), BreadCrumbItem('Profile', 'test_page_two', active=True)]
        breadcrumbs_macro = BreadCrumbMacro("tag_for_breadcrumb_macro", bdi, css_class='test_breadcrumb')

        #tab group macro
        ti = OrderedDict()
        tie = TabItem('e', 'E', external="http://somewhere.com")
        tis = TabItem('s', 'S', static=MacroFor(mwhere='test_macros/test.html', mname='test_macro_static'))
        tii = TabItem('i', 'I', independent=MacroFor(mwhere='test_macros/test.html', mname='test_macro_independent', mattr={'iam': 'independent'}))
        tic = TabItem('c', 'C', content=MacroFor(mwhere='test_macros/test.html', mname='test_macro_tab_content', mattr={'iam': 'content'}))
        tim = TabItem('m', 'M', minimal=MacroFor(mwhere='test_macros/test.html', mname='test_macro_tab_content', mattr={'iam': 'minimal'}))
        tabitems = [tie, tis, tii, tic]
        [ti.update({k.label: k}) for k in tabitems]
        ti2 = ti
        ti2['m'] = tim
        tabs_macro = TabGroupMacro(minimal=False,
                                   tag="tag_for_tab_macro",
                                   tabs_label="test_tabs",
                                   tab_groups=ti)
        minimal_tabs_macro = TabGroupMacro(minimal=True,
                                          tag="tag_for_minimal_tabs",
                                          tabs_label="minimal_test_tabs",
                                          tab_groups=ti2)

        packaged_macros = {'accordian_macro': accordian_macro,
                           'breadcrumbs_macro': breadcrumbs_macro,
                           'tabs_macro': tabs_macro,
                           'minimal_tabs_macro': minimal_tabs_macro}

        @self.app.route('/static_macro')
        def stat_mac():
            return render_template('index.html', rstat=static_macro)

        @self.app.route('/content_macro')
        def con_mac():
            return render_template('index.html', rcont=content_macro, content={'any': "THING"})

        @self.app.route('/attr_macro')
        def sub_mac():
            return render_template('index.html', rattr=attr_macro)

        @self.app.route('/named_macro')
        def nam_mac():
            return render_template('index.html', test_named=True)

        @self.app.route('/<macro_type>')
        def gen_mac(macro_type):
            return render_template('index.html', m=packaged_macros[macro_type])

        @self.app.route('/one')
        def test_page_one():
            return "ONE"

        @self.app.route('/two')
        def test_page_two():
            return "TWO"

        #ul/li links macro
        l1 = LiItem('l1', for_url='test_page_one')
        l2 = LiItem('l2', for_url='test_page_two', arbitrary='for_attr_macro_route')

        links_list = UlMacro([l1, l2])

        packaged_macros.update({'links_list': links_list})


    def tearDown(self):
        self.app = None
