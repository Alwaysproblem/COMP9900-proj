from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class PersonForm(FlaskForm):
    Name = StringField("Name", validators=[DataRequired()])
    Male = BooleanField("Male")
    Female = BooleanField("Female")
    Weight = StringField("Weight", validators=[DataRequired()])
    submit = SubmitField("Submit")

