from wtforms import StringField, SubmitField, MultipleFileField, FileField
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length

class NewsPostForm(FlaskForm):
    """
    Form for creating or updating news articles.
    """
    title = StringField('Title:', name="title", validators=[DataRequired(), Length(max=200)])
    summary = StringField('Summary:', name="summary", validators=[DataRequired(), Length(max=255)])
    images = MultipleFileField('Images:')  # This will allow multiple file uploads, but we will only use the first one as the main image.
    article = CKEditorField('Content:', name="article", validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditPostForm(FlaskForm):
    """
    Form for editing existing news articles.
    """
    summary = StringField('Edit summary:', name="summary", validators=[DataRequired(), Length(max=255)])
    images = MultipleFileField('Edit images:', name="images")  # This will allow multiple file uploads
    article = CKEditorField('Edit content:', name="article", validators=[DataRequired()])
    submit = SubmitField('Update')