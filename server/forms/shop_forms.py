from wtforms import StringField, SubmitField, DecimalField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, NumberRange

class ShopItemForm(FlaskForm):
    """
    Form for creating or updating shop items.
    """
    name = StringField('Name:', name="name", validators=[DataRequired(), Length(max=100)])
    description = StringField('Description:', name="description", validators=[DataRequired()])
    # TODO image support
    price = DecimalField('Price:', name="price", validators=[DataRequired(), NumberRange(min=0.010, message="Price must be a positive number")], places=2, rounding=None)
    submit = SubmitField('Submit')
