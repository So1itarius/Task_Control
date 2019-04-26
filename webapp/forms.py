# -*- coding: utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class TaskForm(FlaskForm):
    headline = StringField('Заголовок задачи', validators=[DataRequired()],render_kw={"class": "form-control",
                                                                                    "aria-label": "Sizing example input",
                                                                                    "aria-describedby": "inputGroup-sizing-default"})
    task = TextAreaField('Описание задачи', validators=[DataRequired()], render_kw={"class": "form-control",
                                                                                    "aria-label": "With textarea"})
    submit = SubmitField('Отправить',render_kw={"class":"btn btn-secondary btn-lg btn-block btn-info"})

class StatusForm(FlaskForm):
    status = TextAreaField('скрытое поле ввода', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения', render_kw={"class": "btn btn-outline-success"})
