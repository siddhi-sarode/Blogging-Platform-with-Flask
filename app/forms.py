from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tags = StringField('Tags (comma-separated)')
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish Post')

class CommentForm(FlaskForm):
    body = TextAreaField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')