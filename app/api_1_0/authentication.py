from flask import g, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from app.models import User, AnonymousUser

from app.main.errors import forbidden
from app.api_1_0 import api

http_auth = HTTPBasicAuth()


@http_auth.verify_password
def verify_password(email_or_token, password):
    #  对于匿名用户，也应该加以"验证"，前提是服务器提交的邮箱字段为空
    """

    :param email_or_token: 可使用令牌或常规登录，对于匿名用户，邮箱字段必须为空
    :param password: 密码，密码为空则使用令牌登录
    :return:
    """
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.query.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    # 常规登录
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@http_auth.error_handler
def unauthorized(msg='Unauthorized Access.'):
    return make_response(jsonify({'error': msg}), 401)


@http_auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/token')
def get_token():
    # 避免用户申请新令牌，只能持有一个令牌
    if g.current_user.is_annoymous() or g.token_used:
        return unauthorized('无效请求')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})


@api.before_request
@http_auth.login_required
def before_request():
    if not g.current_user.is_annoymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed Account')


