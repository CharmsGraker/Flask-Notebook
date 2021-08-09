from flask import Blueprint

blogs = Blueprint('blogs', __name__, template_folder='templates', static_folder='static')

from . import views
