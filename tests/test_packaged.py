def test_list(app):
    rv = app.test_client().get('/links_list')
    assert b'l1' in rv.data
    assert b'href="/one"' in rv.data
    assert b'arbitrary=for_attr_macro_route' in rv.data
    assert b'a plain item' in rv.data


def test_accordion_default(app):
    rv = app.test_client().get('/accordion_macro')
    assert b'class="accordion-group accordionset"' in rv.data
    assert b'data-parent="#accordionset"' in rv.data


def test_accordion_minimal(app):
    rv = app.test_client().get('/minimal_accordion_macro')
    assert b'heading=accordion4' in rv.data


def test_tabs_default(app):
    rv = app.test_client().get('/tabs_macro')
    assert b'class="tabset"' in rv.data
    assert b'tab-content' in rv.data


def test_tabs_minimal(app):
    rv = app.test_client().get('/minimal_tabs_macro')
    assert b'tabset' in rv.data
    assert b'minimal' in rv.data
