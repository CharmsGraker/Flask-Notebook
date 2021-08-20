from flask import Blueprint

auth = Blueprint('auth', 'auth', template_folder='app/auth/templates',
                 static_folder='app/auth/static')  # 需要手动设置static_folder

from . import views
