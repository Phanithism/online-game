from flask_wtf import Form
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired, EqualTo


class RegistrationForm(Form):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('confirmation_password')])
    confirmation_password = PasswordField('Confirmation Password', validators = [DataRequired()])

class LoginForm(Form):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])

class GameForm(Form):
    name = StringField("Game's Name", validators = [DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    embed_url = StringField("Embed Url", validators = [DataRequired()])
    logo =  FileField('Game Logo', validators = [DataRequired()])
