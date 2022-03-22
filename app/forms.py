from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, TextAreaField

class Add_Property(FlaskForm):
    property_title = StringField("Property Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    no_of_rooms = StringField("No. of Rooms", validators=[DataRequired()], render_kw={"rows": 4})
    no_of_bathrooms = StringField("No. of Bathrooms", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    property_type = SelectField("Property Type", choices=["House", "Apartment"])
    location = StringField("Location", validators=[DataRequired()])
    photo = FileField("Photo", validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg'], 'Incorrect file type.')])
