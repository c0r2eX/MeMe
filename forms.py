from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import PasswordField
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class Memeupload(FlaskForm):
    text = StringField("Text", validators=[DataRequired()])
    img = FileField("Image URL", validators=[DataRequired()])
    text_color = SelectField(
        "Text Color",
        choices=[("black", "Black"), ("red", "Red"), ("blue", "Blue"), ("green", "Green"), ("yellow", "Yellow")],
        default="black",
    )
    submit = SubmitField("Upload Meme")
    
class Register(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    repeat_password = PasswordField("Repeat Password", validators=[EqualTo("password", message="Passwords must match.")])
    register_submit = SubmitField()

class Login(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    login_submit = SubmitField("LOGIN")
