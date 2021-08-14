from wtforms import Form
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, IntegerField,validators
from wtforms.validators import DataRequired, Length, Regexp


class ArticleForm(Form):
    title = StringField(validators=[DataRequired(), validators.Length(min=3, max=25, message='标题长度在3至25之间')])
    content = TextAreaField(validators=[DataRequired()])
    author = StringField()
    create_date = DateTimeField()


class DeleteArticleForm(Form):
    submit = SubmitField('删除')


