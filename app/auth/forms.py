from wtforms import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Regexp, Email


class RegisterForm(Form):
    username = StringField("你的名字是?", validators=[
        DataRequired(message='用户名不能为空'), Length(min=2, max=25, message='用户名在2至25个字符内'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField('电子邮箱', [DataRequired(message='请填写邮箱'), Length(min=6, max=35)])
    password = PasswordField("密码", [validators.Length(min=8, max=16, message='密码在8至16个字符内')])
    password_confirm = PasswordField("请确认密码",
                                     [validators.Length(min=8, max=16, message='密码在8至16个字符内')])
    submit = SubmitField('登录')


class LoginForm(Form):
    username = StringField("用户名", [validators.Length(min=2, max=25, message='用户名在2至25个字符内')])
    password = PasswordField("密码", [validators.Length(min=8, max=16, message='密码在8至16个字符内')])
    remember_me = BooleanField()
    submit = SubmitField('登录')
