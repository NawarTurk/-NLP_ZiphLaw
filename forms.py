from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class FileUploadForm(FlaskForm):
    file = FileField('Upload Text File', validators=[FileRequired(), FileAllowed(['txt'], 'Text files only!')])
    submit = SubmitField('Submit & Analyze')