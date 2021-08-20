from flask import Blueprint

community = Blueprint('community', 'community',
               template_folder='app/community/templates',
               static_folder='app/community/static')  # 需要手动设置static_folder

from . import views
