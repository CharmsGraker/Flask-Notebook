from flask import render_template, request, session, redirect, url_for, flash, g
from flask_login import login_required, current_user, login_user, logout_user
from ..models import User
from app import db
from . import auth
from .forms import RegisterForm, LoginForm
from .. import send_email


@auth.app_context_processor
def context():
    return dict(zip=zip)


@auth.before_app_request
def before_request():
    # 拦截去其他网页的访问
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static' \
                and request.endpoint[:7] != 'profile':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/confirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_info(token):
        flash('你已成功确认。Thank U~', 'success')
    else:
        flash('确认链接已失效', 'info')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    print(token)
    send_email(current_user.email, '请确认账户', 'email/confirm', user=current_user, token=token)
    flash('一封新的确认邮件已发送，请查收后激活您的账号', 'info')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('email/unconfirmed.html', user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(url_for('users.dashboard') or url_for('main.index'))
            else:
                flash('账号密码错误', 'warning')
        else:
            flash('无效的用户账号，请重试', 'danger')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        exist_user = User.query.filter_by(username=form.username.data).first()
        if exist_user:
            flash('该用户名已被注册', 'warning')
        else:
            user = User(email=form.email.data, username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(to=user.email, subject='请确认你的Notebook账号', template='email/confirm', user=user, token=token)

            flash('我们已向你发送了一封邮件，请确认', 'success')
            return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash('您已成功退出', 'warning')
    return redirect(url_for('main.index'))
