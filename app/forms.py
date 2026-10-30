from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

from wtforms import TextAreaField

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')