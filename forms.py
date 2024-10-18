from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadImageForm(FlaskForm):
    image = FileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField('Upload')