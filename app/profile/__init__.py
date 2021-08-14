from flask import Blueprint

profile = Blueprint('profile', 'profile', static_folder='static', template_folder='templates')

from . import views