"""
Flask-Macro4
-------------
A tool for working with template macros in flask/jinja2 plus assorted useful
pre-built macros
"""
from setuptools import setup
from flask_macro4 import __version__

setup(
    name='Flask-Macro4',
    version=__version__,
    url='https://github.com/thrisp/flask_macro4',
    license='BSD',
    author='hurrata/thrisp',
    author_email='blueblank@gmail.com',
    description='flask/jinja2 templating tools',
    long_description=__doc__,
    packages=['flask_macro4'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask >= 0.9',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test',
    tests_require=['blinker'],
)
