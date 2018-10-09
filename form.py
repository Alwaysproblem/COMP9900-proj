from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, SelectField, DateField, MultipleFileField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, email, optional, required, length
from werkzeug.utils import secure_filename

class PersonForm(FlaskForm):
    UserEmail = StringField(
            "UserEmail", 
            validators = [
                DataRequired(), 
                email(message="please imput an email address not a joke.")
            ])
    HouseID = StringField("HouseID")
    Room = StringField("Room Number", validators=[DataRequired()])
    Street = StringField("Street", validators=[DataRequired()])
    Suburb = StringField("Suburb", validators=[DataRequired()])
    State = StringField("State", validators=[DataRequired()])
    Postcode = StringField("Postcode", validators=[DataRequired()])
    RoomType = SelectField(
            "Room Type", 
            validators=[DataRequired()],
            choices=[
                ("Single Room", "Single Room"),
                ("Double Room", "Double Room"),
                ("Multiple Rooms", "Multiple Rooms")
            ]
        )
    Star = SelectField(
                "Star Ratings", 
                validators=[DataRequired()],
                choices=[
                    ('1', '*'),
                    ('2', '**'),
                    ('3', '***'),
                    ('4', '****'),
                    ('5', '*****')
                ])
    check_in_date = DateField(
                "CheckIn Date(MM/DD/YY)", 
                validators=[DataRequired()],
                format="%m/%d/%Y")
    check_out_date = DateField(
                "CheckOut Date(MM/DD/YY)", 
                validators=[DataRequired()],
                format="%m/%d/%Y")
    Price = IntegerField("Renting Price per day", validators=[DataRequired()])
    Description = TextAreaField("Description", validators=[optional(), length(max=250)])
    Image = FileField("image", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Submit")

