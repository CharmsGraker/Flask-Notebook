from flask import Blueprint

spending = Blueprint('spending', 'spending', static_folder='app/spending/static', template_folder='app/spending/templates')

from . import views