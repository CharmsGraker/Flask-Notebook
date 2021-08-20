from wtforms import Form, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(Form):
    body = TextAreaField('Whats your opinion?', validators=[DataRequired()])
    submit = SubmitField('Submit')