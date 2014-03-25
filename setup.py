"""
Flask-Macro4
-------------
A tool for working with template macros in flask/jinja2 plus assorted useful
pre-built macros
"""
from setuptools import setup

setup(
    name='Flask-Flacro',
    version='0.0.8',
    url='https://github.com/thrisp/flacro',
    license='MIT',
    author='hurrata/thrisp',
    author_email='blueblank@gmail.com',
    description='flask/jinja2 templating tools',
    long_description=__doc__,
    packages=['flask_flacro'],
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
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'blinker'],
)
