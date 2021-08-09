import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN') or '845919088@qq.com'

    @staticmethod
    def init_app(app):
        # 占位用
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # 邮箱相关
    MAIL_SERVER = 'smtp.qq.com'  # 使用的邮箱服务器
    MAIL_PORT = 25  # 端口   支持SSL一般为465，默认为25
    # MAIL_USE_SSL = True  # 是否支持SSL
    MAIL_USE_TLS = True  # 是否支持TLS
    MAIL_DEBUG = True
    # MAIL_DEFAULT_SENDER = 'xxx@163.com'  # 默认发件人
    MAIL_USERNAME = '845919088@qq.com'# os.environ.get('MAIL_USERNAME')  # 用户名
    MAIL_PASSWORD = 'pvytpbwtmhqzbcaj'# os.environ.get('MAIL_PASSWORD')  or 163邮箱客户端授权码，不是登录密码
    MAIL_DEFAULT_SENDER = ('CG', '845919088@qq.com')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <845919088@qq.com>'

    #会话相关
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


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
