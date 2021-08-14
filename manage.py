import os

from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 'FLASK_CONFIG'不是必须的
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app.models import User, Role, Post, Follow, Permission


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Follow=Follow, Permission=Permission)


manager.add_command('shell', Shell(make_context=make_shell_context))  # 传入函数名
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        print([sys.executable] + sys.argv)
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    case_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    tests = unittest.TestLoader().discover(case_path, 'tests')  # 需要指定下目录
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
    """
    0 (quiet): 只显示执行的用例的总数和全局的执行结果。
1 (default): 默认值，显示执行的用例的总数和全局的执行结果，并对每个用例的执行结果（成功 T 或失败 F）有个标注。
2 (verbose): 显示执行的用例的总数和全局的执行结果，并输出每个用例的详细的执行结果。
    """


@manager.command
def deploy():
    """

    :return:
    """
    from flask_migrate import upgrade
    from app.models import Role, User

    upgrade()

    # 创建新加的角色
    Role.insert_roles()

    # 让所有用户关注自己
    User.add_self_follows()


if __name__ == '__main__':
    # 确保是单独运行该模块
    manager.run()
