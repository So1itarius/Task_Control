# -*- coding: utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from webapp.model import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')


class TaskForm(FlaskForm):
    headline = StringField('Заголовок задачи', validators=[DataRequired()], render_kw={"class": "form-control",
                                                                                       "aria-label": "Sizing example input",
                                                                                       "aria-describedby": "inputGroup-sizing-default"})
    task = TextAreaField('Описание задачи', validators=[DataRequired()], render_kw={"class": "form-control",
                                                                                    "aria-label": "With textarea"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-secondary btn-lg btn-block btn-info"})


class StatusForm(FlaskForm):
    status = TextAreaField('скрытое поле ввода', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения', render_kw={"class": "btn btn-outline-success"})
