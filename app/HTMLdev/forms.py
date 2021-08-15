from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed

accept_extension = []


class UploadImgForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileRequired(), FileAllowed(accept_extension)])
    submit = SubmitField()
