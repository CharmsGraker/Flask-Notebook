from flask import Blueprint

dev = Blueprint('dev', 'dev', template_folder='app/HTMLdev/templates', static_folder='app/HTMLdev/static')
# Blueprint要求至少传入两个参数，分别是蓝图的名字和蓝图所在的包或模块。

from . import views