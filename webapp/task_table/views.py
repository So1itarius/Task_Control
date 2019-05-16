from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user

from webapp.task_table.forms import TaskForm, StatusForm
from webapp.user.models import User
from webapp.task_table.models import Tasks

from webapp.db import db

blueprint = Blueprint('board', __name__)


@blueprint.route('/')
def index():
    form = TaskForm()
    form1 = StatusForm()
    data = [row for row in db.engine.execute(f"SELECT id,title,text,user_id FROM Tasks")]
    if current_user.is_authenticated:
        data1 = [row for row in db.engine.execute(f"SELECT status FROM User WHERE id=={current_user.id}")]
        jq_form_id = data1[0][0][2:-2].replace("', '", ", ")
    else:
        return render_template('task_table/index.html', form=form, data=data, user_id=None)
    return render_template('task_table/index.html', form=form, data=data, user_id=current_user.id, form1=form1,
                           jq_form_id=jq_form_id)


@blueprint.route('/process-task', methods=['POST'])
def process_task():
    form = TaskForm()
    if current_user.is_authenticated and form.validate_on_submit():
        new_task = Tasks(user_id=current_user.id, title=form.headline.data, text=form.task.data)
        db.session.add(new_task)
        db.session.commit()
        flash('Вы успешно добавили задачу!')
        return redirect(url_for('board.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(form, field).label.text}": - {error}')

        return redirect(url_for('board.index'))


@blueprint.route('/process-status', methods=['POST'])
def process_status():
    if current_user.is_authenticated:
        check_list = request.form.getlist('vehicle1')
        User.query.filter_by(id=current_user.id) \
            .update({'status': f'{check_list}'})
        db.session.commit()
        flash('Настройки сохранены!')
        return redirect(url_for('board.index'))
    else:
        return redirect(url_for('board.index'))
