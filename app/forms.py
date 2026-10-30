from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

from wtforms import TextAreaField

class CommentForm(FlaskForm):
    body = TextAreaField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')