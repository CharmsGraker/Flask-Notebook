from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from threading import Thread
from flask_pagedown import PageDown

from config import config
import os

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


bootstrap = Bootstrap()
mail = Mail()
app = Flask(__name__)
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
pagedown = PageDown()


# 注意括号，不然调用不了构造实例
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录噢 OWO'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)

    # 在这里注册所有蓝本
    from .api_1_0 import api as api_1_0_blueprint

    from .main import main as main_blueprint
    from .users import users as user_blueprint
    from .auth import auth as auth_blueprint
    from .profile import  profile as profile_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(profile_blueprint,url_prefix='/profile')

    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)  # 以传入需要的用户名和token
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr





