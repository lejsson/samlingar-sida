from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User
from PIL import Image

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description (optional)')
    image = FileField('General image for the post', validators=[DataRequired()])
    submit = SubmitField('Add post')

class NewPostContentForm(FlaskForm):
    title = StringField('Title (optional)')
    description = StringField('Description (optional)')
    image = FileField('Image for the post content', validators=[DataRequired()])
    submit = SubmitField('Add content')
