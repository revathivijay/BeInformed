from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired,  ValidationError, Email
from Main.models import Student, Faculty, Post
from flask_login import current_user




class LoginForm(FlaskForm):

    #email = StringField('Email', validators = [DataRequired(),Email()])
    id = IntegerField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class AddStudents(FlaskForm):

    id = IntegerField('ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators = [DataRequired(),Email()])
    submit = SubmitField("Submit")
    def validate_id(self, id):
        student = Student.query.filter_by(id = id.data).first()
        if student:
            raise ValidationError("This ID is taken choose another one")

    def validate_email(self, email):
        student = Student.query.filter_by(email = email.data).first()
        if student:
            raise ValidationError("This Email is taken choose another one")


class AddFaculties(FlaskForm):

    id = IntegerField('ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    course = StringField('Course', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")
    def validate_id(self, id):
        faculty = Faculty.query.filter_by(id = id.data).first()
        if faculty:
            raise ValidationError("This ID is taken choose another one")

    def validate_email(self, email):
        faculty = Faculty.query.filter_by(email= email.data).first()
        if faculty:
            raise ValidationError("This Email is taken choose another one")

class UpdateAccountForm(FlaskForm):

    name = StringField('Name', validators=[])
    email = StringField('Email', validators=[Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Update")

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
