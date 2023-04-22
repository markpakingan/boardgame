from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):

    """Form for adding users"""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class GameListForm(FlaskForm):

    title = StringField("GameList Title",validators=[DataRequired()])
    name = StringField("Name",validators=[DataRequired()])
    description = StringField("Description",validators=[DataRequired()])


class ReviewForm(FlaskForm):
    rating = SelectField("Rating", choices =[("1", "1"), ("2", "2"),
                                            ("3", "3"),("4", "4"),
                                            ("5", "5")] , 
                                            validators=[DataRequired()])
    feedback = StringField("Feedback", validators=[DataRequired()])
    
class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""