import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    # 邮箱相关
    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN') or '845919088@qq.com'

    MAIL_SERVER = 'smtp.qq.com'  # 使用的邮箱服务器
    MAIL_PORT = 25  # 端口   支持SSL一般为465，默认为25
    # MAIL_USE_SSL = True  # 是否支持SSL
    MAIL_USE_TLS = True  # 是否支持TLS
    MAIL_DEBUG = True

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 用户名
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 163邮箱客户端授权码，不是登录密码

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <845919088@qq.com>'

    # MAIL_DEFAULT_SENDER = 'xxx@163.com'  # 默认发件人
    MAIL_DEFAULT_SENDER = ('CG', '845919088@qq.com')

    # SSL
    SSL_DISABLE = True

    # 会话相关
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    # 数据库相关
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)

    # 分页相关
    FLASKY_POSTS_PER_PAGE = 15
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        # 占位用
        pass


class DevelopmentConfig(Config):
    DEBUG = True



class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    # CSRF认证
    WTF_CSRF_ENABLED = False





class ProductionConfig(Config):

    # classmethod 类对象不需要实例化
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler

        credentials = None
        secure = None

        if getattr(cls, 'MAIL_USERNAME',None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + 'Application Error',
            credentials=credentials,
            secure=secure)

        # 当出现严重ERROR才发邮件给ADMIN
        mail_handler.setLevel(logging.ERROR)
        # 注册到app的logger handler
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # 处理日志
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        # 处理安全等级，因为反向代理服务器的原因
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig
}