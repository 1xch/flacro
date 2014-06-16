def test_macro_static(app):
    rv = app.test_client().get('/static_macro')
    assert b'STATIC MACRO' in rv.data


def test_macro_content(app):
    rv = app.test_client().get('/content_macro')
    assert b'THING' in rv.data


def test_macro_attr(app):
    rv = app.test_client().get('/attr_macro')
    assert b'abc' in rv.data


def test_macro_named(app):
    rv = app.test_client().get('/named_macro')
    assert b'A NAMED MACRO RENDERED BY NAME' in rv.data
    assert b'123' in rv.data
