from flask_wtf import Form 
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class RegisterForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])

class PostForm(Form):
    title = StringField("title", validators=[DataRequired()])
    vaga = StringField("vaga", validators=[DataRequired()])
    salario = StringField("salario", validators=[DataRequired()])
    content = TextAreaField("content", validators=[DataRequired()])
    contato = TextAreaField("contato", validators=[DataRequired()])

