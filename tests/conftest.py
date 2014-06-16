from collections import OrderedDict

import pytest

from flask import Flask, render_template
from flask_flacro import (Flacro, FlacroFor, AccordionItem, AccordionGroupMacro,
                          TabItem, TabGroupMacro, LiItem, ListMacro)


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    Flacro(app)
    app.debug = True
    static_macro = FlacroFor(tag='static_macro', mwhere='test_macros/test.html', mname='test_macro_static')
    content_macro = FlacroFor(tag='content_macro', mwhere='test_macros/test.html', mname='test_macro_with_content')
    named_macro = FlacroFor(tag='named_macro', mwhere='test_macros/test.html', mname='test_named_macro')

    class TestSubclass(FlacroFor):
            def __init__(self, anything, **kwargs):
                self.anything = anything
                super(TestSubclass, self).__init__(tag=kwargs.get('tag', None),
                                                   mwhere='test_macros/test.html',
                                                   mname='test_macro_with_attr')

    attr_macro = TestSubclass("abc", tag="ATTR_MACRO_1")
    attr_macro_alternate = TestSubclass("123", tag="ATTR_MACRO_2")

    # accordion macro
    ai = []
    for i in range(5):
        ai.append(AccordionItem("accordion{}".format(i), FlacroFor(tag="inner_{}".format(i), mwhere='test_macros/test.html', mname='test_macro_tab_content', mattr={'iam': 'content'})))
    accordion_macro = AccordionGroupMacro(ai, kind='bootstrap')
    minimal_accordion_macro = AccordionGroupMacro(ai)

    # tab group macro
    ti = OrderedDict()
    tie = TabItem('e', 'E', external="http://somewhere.com")
    tis = TabItem('s', 'S', static=FlacroFor(mwhere='test_macros/test.html', mname='test_macro_static'))
    tii = TabItem('i', 'I', independent=FlacroFor(mwhere='test_macros/test.html', mname='test_macro_independent', mattr={'iam': 'independent'}))
    tic = TabItem('c', 'C', content=FlacroFor(mwhere='test_macros/test.html', mname='test_macro_tab_content', mattr={'iam': 'content'}))
    tim = TabItem('m', 'M', minimal=FlacroFor(mwhere='test_macros/test.html', mname='test_macro_tab_content', mattr={'iam': 'minimal'}))
    tabitems = [tie, tis, tii, tic]
    [ti.update({k.label: k}) for k in tabitems]
    ti2 = ti
    ti2['m'] = tim
    tabs_macro = TabGroupMacro(ti, kind='bootstrap')
    minimal_tabs_macro = TabGroupMacro(ti2)

    # list/listitems macro
    l1 = LiItem('l1', kind='link', for_url='test_page_one')
    l2 = LiItem('l2', kind='link', for_url='test_page_two', arbitrary='for_attr_macro_route')
    l3 = LiItem('a plain item')

    links_list = ListMacro([l1, l2, l3])

    packaged_macros = {'accordion_macro': accordion_macro,
                       'minimal_accordion_macro': minimal_accordion_macro,
                       'tabs_macro': tabs_macro,
                       'links_list': links_list,
                       'named_macro': named_macro,
                       'minimal_tabs_macro': minimal_tabs_macro,
                       'attr_macro': attr_macro,
                       'attr_macro_alternate': attr_macro_alternate}

    @app.route('/static_macro')
    def stat_mac():
        return render_template('index.html', rstat=static_macro)

    @app.route('/content_macro')
    def con_mac():
        return render_template('index.html', rcont=content_macro, content={'any': "THING"})

    @app.route('/attr_macro')
    def sub_mac():
        return render_template('index.html', rattr=attr_macro)

    @app.route('/named_macro')
    def nam_mac():
        return render_template('index.html', test_named=True)

    @app.route('/<macro_type>')
    def gen_mac(macro_type):
        return render_template('index.html', m=packaged_macros[macro_type])

    @app.route('/one')
    def test_page_one():
        return "ONE"

    @app.route('/two')
    def test_page_two():
        return "TWO"

    return app
