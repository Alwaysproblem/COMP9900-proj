from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, SelectField, DateField, MultipleFileField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, email
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
                ("Multiple Room", "Multiple Room")
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
                "CheckIn Date(DD/MM/YY)", 
                validators=[DataRequired()],
                format="%d/%m/%Y")
    check_out_date = DateField(
                "CheckOut Date(DD/MM/YY)", 
                validators=[DataRequired()],
                format="%d/%m/%Y")
    Price = IntegerField("Renting Price per week", validators=[DataRequired()])
    Description = StringField("Description", validators=[DataRequired()])
    Image = FileField("image", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    # Image = MultipleFileField(
    #             "image", 
    #             validators=[
    #                 FileRequired(), 
    #                 FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    #             ]
    #         )
    submit = SubmitField("Submit")

