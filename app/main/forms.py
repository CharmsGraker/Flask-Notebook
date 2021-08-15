from wtforms import Form, validators, StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired, Regexp


class ModifyForm(Form):
    email = StringField('电子邮箱', [DataRequired(message='更改邮箱'), Length(min=6, max=35)])
    username = StringField('昵称', [DataRequired(message='更改昵称'), Length(min=2, max=35, message='用户名在2至25个字符内'),
                                  Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                         '    Usernames must have only letters, numbers, dots or underscores')])


class EditProfileForm(Form):
    username = StringField('昵称', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('提交')


class PostForm(Form):
    body = TextAreaField('Whats your opinion?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = TextAreaField('评论', validators=[DataRequired(), Length(min=3, max=400)])
    submit = SubmitField('提交评论')


class DeletePostForm(Form):
    submit = SubmitField('删除留言')
