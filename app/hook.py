# from flask import current_app
#
# from app import app
# from app.spending.labelHash import LabelProjection
#
#
# @app.before_first_request
# def before_app_first_request():
#     print('load-----------------------')
#     config_path = current_app.config['SPENDING_LABEL_HASH_DIR']
#     g.label_hash = LabelProjection(path_prefix=config_path)