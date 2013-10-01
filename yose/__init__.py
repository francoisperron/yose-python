from flask import Flask
import os

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')

app = Flask(__name__, template_folder=tmpl_dir, static_folder=static_folder)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

import ui
import api