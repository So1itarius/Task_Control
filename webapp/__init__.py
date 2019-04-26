import ast

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate

from jinja2 import Environment, DictLoader

from webapp.forms import LoginForm, TaskForm, StatusForm
from webapp.model import db, User, Tasks


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        form = TaskForm()
        form1 = StatusForm()
        data = [row for row in db.engine.execute(f"SELECT id,title,text,user_id FROM Tasks")]
        if current_user.is_authenticated:
            #print(current_user.id)
            #print(current_user.username)
            data1 = [row for row in db.engine.execute(f"SELECT status FROM User WHERE id=={current_user.id}")]
            # print(data)
            l = data1[0][0][2:-2].replace("', '", ", ")
            #print(l)
            # print(ast.literal_eval(data1[0][0])[0])
            # user_id = [row[0] for row in db.engine.execute(f"SELECT id,username FROM User WHERE username=='{current_user}'")][0]
            # print( user_id )
        else:
            return render_template('index.html', form=form, data=data, user_id=None)
        # result = db.engine.execute(f"SELECT id,username FROM User WHERE username=='{current_user}'")
        # names = [row[0] for row in result]
        # print(current_user)
        # print(data)

        # print(user_id)
        return render_template('index.html', form=form, data=data, user_id=current_user.id, form1=form1, l=l)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # @app.route('/task')
    # def task():
    #
    #    return render_template('task.html')

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        if login_form.validate_on_submit():
            flash(f'Login requested for user {login_form.username.data}, remember_me={login_form.remember_me.data}')
            return redirect(url_for('index'))
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                # return render_template('index.html', user=user)
                return redirect(url_for('index'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/process-task', methods=['POST'])
    def process_task():
        form = TaskForm()
        if current_user.is_authenticated and form.validate_on_submit():
            new_task = Tasks(user_id=[row[0] for row in db.engine.execute(
                f"SELECT id,username FROM User WHERE username=='{current_user}'")][0],
                             title=form.headline.data, text=form.task.data)
            db.session.add(new_task)
            db.session.commit()
            flash('Вы успешно добавили задачу!')
            return redirect(url_for('index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Ошибка в поле "{getattr(form, field).label.text}": - {error}')

            return redirect(url_for('index'))

    @app.route('/process-status', methods=['POST'])
    def process_status():
        # form = StatusForm()
        if current_user.is_authenticated:
            # and \
            # form.validate_on_submit():
            r = request.form.getlist('vehicle1')
            print(r)
            User.query.filter_by(id=current_user.id) \
                .update({'status': f'{r}'})
            db.session.commit()
            flash('Настройки сохранены!')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    return app
