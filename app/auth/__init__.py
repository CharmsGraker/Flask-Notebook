from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates',static_folder='static')  # 需要手动设置static_folder

from . import views
