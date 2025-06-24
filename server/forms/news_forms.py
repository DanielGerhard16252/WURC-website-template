from wtforms import StringField, SubmitField
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

class NewsPostForm(FlaskForm):
    """
    Form for creating or updating news articles.
    """
    title = StringField('Title:', name="title", validators=[DataRequired(), Length(max=200)])
    summary = StringField('Summary:', name="summary", validators=[DataRequired(), Length(max=255)])
    # TODO image support
    content = CKEditorField('Content:', name="content", validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditPostForm(FlaskForm):
    """
    Form for editing existing news articles.
    """
    summary = StringField('Edit summary:', name="summary", validators=[DataRequired(), Length(max=255)])
    content = CKEditorField('Edit content:', name="content", validators=[DataRequired()])
    submit = SubmitField('Update')