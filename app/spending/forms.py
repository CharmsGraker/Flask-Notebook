from datetime import datetime

from wtforms import Form
from wtforms import StringField, TextAreaField, SubmitField, FloatField, BooleanField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Length, Regexp

from wtforms.fields.html5 import DateTimeLocalField
from flask_wtf.file import FileField, FileSize, FileAllowed


class SpendingRecordForm(Form):
    title = StringField(validators=[DataRequired(), Length(min=1, max=15, message='标题长度在3至15之间')], default='Untitled')

    # 在提交时进行验证大小好了
    banner_image = FileField(validators=[ FileAllowed(['jpg', 'png', 'jpeg'])])
    costs = FloatField(validators=[DataRequired()], default=-1)
    description = TextAreaField(default='empty text')
    spending_tag = IntegerField(validators=[DataRequired(), InputRequired()], default=0)
    # 这个是指用户记账中提到的时间，不是这条记录的创建时间
    spending_record_date = DateTimeLocalField(format='%Y-%m-%dT%H:%M')

    public = BooleanField(default=True)
    submit = SubmitField()
