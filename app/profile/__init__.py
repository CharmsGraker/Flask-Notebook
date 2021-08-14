from flask import Blueprint

profile = Blueprint('profile', __name__, static_folder='static', template_folder='templates')

from . import views