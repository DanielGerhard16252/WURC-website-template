from wtforms import StringField, SubmitField, DecimalField, MultipleFileField
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, NumberRange

class ShopItemForm(FlaskForm):
    """
    Form for creating or updating shop items.
    """
    name = StringField('Name:', name="name", validators=[DataRequired(), Length(max=100)])
    description = CKEditorField('Description:', name="description", validators=[DataRequired()])
    images = MultipleFileField("Images:")
    price = DecimalField('Price:', name="price", validators=[DataRequired(), NumberRange(min=0.010, message="Price must be a positive number")], places=2, rounding=None)
    submit = SubmitField('Submit')
