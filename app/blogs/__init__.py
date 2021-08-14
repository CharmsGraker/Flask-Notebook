from flask import Blueprint

blogs = Blueprint('blogs', 'blogs', template_folder='app/blogs/templates', static_folder='static')

from . import views
