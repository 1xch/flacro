from unittest import TestCase
from flask import Flask, render_template, current_app
from flask_macro4 import Macro4

class Macro4Test(TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        Macro4(app)
        self.app = app
