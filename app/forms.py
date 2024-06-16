from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validators.Length(min=1, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validators.Length(min=1, max=20)])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), validators.Length(min=1, max=30)])
    description = StringField('Description (optional)', validators=[validators.Length(max=200)])
    image = FileField('General image for the collection', validators=[DataRequired()])
    submit = SubmitField('Add collection')

class NewPostContentForm(FlaskForm):
    title = StringField('Title (optional)', validators=[validators.Length(max=30)])
    description = StringField('Description (optional)', validators=[validators.Length(max=200)])
    image = FileField('Image for the post', validators=[DataRequired()])
    submit = SubmitField('Add post')

class EditPostForm(FlaskForm):
    new_title = StringField('New title', validators=[DataRequired(), validators.Length(max=30)])
    new_desc = StringField('Updated Description', validators=[validators.Length(max=200)])
    new_image = FileField('New general image for the collection (leave blank to keep the same image)')
    submit = SubmitField('Edit collection')

class EditPostContentForm(FlaskForm):
    new_title = StringField('New title', validators=[validators.Length(max=30)])
    new_desc = StringField('New Description', validators=[validators.Length(max=200)])
    new_image = FileField('New image for the post (leave blank to keep the same image)')
    submit = SubmitField('Edit post')
