from flask import Blueprint

users = Blueprint('users', __name__, template_folder='templates')
# Blueprint要求至少传入两个参数，分别是蓝图的名字和蓝图所在的包或模块。

from . import views
# 在末尾导入是为了避免循环依赖
