
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_migrate import Migrate


from webapp.forms import LoginForm, TaskForm, StatusForm, RegistrationForm
from webapp.model import db, User, Tasks
from webapp.utils import get_redirect_target


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
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
            data1 = [row for row in db.engine.execute(f"SELECT status FROM User WHERE id=={current_user.id}")]
            jq_form_id = data1[0][0][2:-2].replace("', '", ", ")
        else:
            return render_template('index.html', form=form, data=data, user_id=None)
        return render_template('index.html', form=form, data=data, user_id=current_user.id, form1=form1, jq_form_id=jq_form_id)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(get_redirect_target())
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        title = "Регистрация"
        return render_template('registration.html', page_title=title, form=form)

    @app.route('/process-reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, role='user', status='[]')
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!')
            return redirect(url_for('login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Ошибка в поле "{getattr(form, field).label.text}": - {error}')

            return redirect(url_for('register'))


    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/process-task', methods=['POST'])
    def process_task():
        form = TaskForm()
        if current_user.is_authenticated and form.validate_on_submit():
            new_task = Tasks(user_id=current_user.id, title=form.headline.data, text=form.task.data)
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
        if current_user.is_authenticated:
            check_list = request.form.getlist('vehicle1')
            User.query.filter_by(id=current_user.id) \
                .update({'status': f'{check_list}'})
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
