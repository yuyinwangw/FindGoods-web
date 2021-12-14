from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
# from wtforms import ValidationError
# from flask_pagedown.fields import PageDownField
# from ..models import Role, User


class LoginForm(FlaskForm):
    username = StringField('What is your name?', validators=[Length(min=1, max=12,message='Not Null'), DataRequired(message='Not Null')])
    password = PasswordField('password', validators=[Length(min=4, max=12, message='Not Null'), DataRequired(message='Not Null')])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username_r = StringField('What is your name?', validators=[Length(min=1, max=12, message='Not Null'), DataRequired(message='Not Null')])
    password_r = PasswordField('password', validators=[Length(min=4, max=12, message='Not Null'), DataRequired(message='Not Null')])
    email = EmailField('What is your name?', validators=[Length(min=1, max=12, message='Not Null'), DataRequired(message='Not Null')])
    sex = SelectField(u'Sex', choices=[('male', '男'), ('female', '女')], validators=[DataRequired(message='Not Null')])
    age = IntegerField(u'Age', validators=[Length(min=1, max=3, message='Not Null'), DataRequired(message='Not Null')])
    area = SelectField(u'Area', choices=[('Taipei', '台北市'), ('New_Taipei', '新北市'), ('Keelung', '基隆市')])
    career = StringField(u'Career', validators=[Length(min=1, max=10, message='Not Null'), DataRequired(message='Not Null')])
    remember_me_r = BooleanField('Keep me logged in')
    submit_r = SubmitField('Submit')