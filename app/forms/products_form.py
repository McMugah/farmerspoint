from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])  # Add validation for file type
    submit = SubmitField('Submit')
