import os
from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

import forms
import models

UPLOAD_FOLDER = 'static/public/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = '1234567890'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    games = models.Game.select()
    return render_template('index.html', games = games)

@app.route('/user/register', methods = ['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash('successfully register a user', 'success')
        models.User.new(username = form.username.data, password = form.password.data)
        return redirect(url_for('index'))

    return render_template('user/register.html', form = form)

@app.route('/user/login', methods = ['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Could not found email or password", "alert")
            return render_template("user/login.html", form = form)
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('successfully authenticated!')
                return redirect(url_for("index"))
            else:
                flash('Could not found email or password')
                return render_template("user/login.html", form = form)
    else:
        return render_template("user/login.html", form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def uploaded_image():
    file = request.files['logo']
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename

@app.route('/new_game', methods = ['GET', 'POST'])
@login_required
def new_game():
    form = forms.GameForm()
    if form.validate_on_submit():
        filename = uploaded_image()
        models.Game.create(
                    name = form.name.data, description = form.description.data,
                    logo = filename, embed_url = form.embed_url.data,
                    user = g.user._get_current_object()
                    )
        flash("successfully added a game", 'notice')
        return redirect(url_for('index'))
    elif form.validate_on_submit() is not True and request.method == 'POST':
        flash('Failed to add a new game', 'alert')
        return render_template('game/new_game.html', form = form)
    else:
        return render_template('game/new_game.html', form = form)

@app.route('/game/<name>/edit_game', methods = ['GET', 'POST'])
@login_required
def edit_game(name = None):
    try:
        game = models.Game.get(models.Game.name == name)
        form = forms.GameForm(obj = game)
        print(request.method)
        if request.method == 'POST':
            if form.validate_on_submit():
                filename = uploaded_image()
                game.name = form.name.data,
                game.description = form.description.data
                game.embed_url = form.embed_url.data
                game.logo = filename
                game.save()
                flash("successfully edited a game", 'notice')
                return redirect(url_for('index'))
            else:
                flash('Failed to update a game', 'alert')
                return render_template('game/edit_game.html', form = form, game = game)
        else:
            print(request.method)
            return render_template('game/edit_game.html', form = form, game = game)
    except models.DoesNotExist:
        flash('Could not found record to update')
        return redirect(url_for('my_games'))

@app.route('/game/<name>')
def game(name = None):
    game = models.Game.get(models.Game.name == name)
    return render_template('game/game.html', game = game)

@app.route('/my_games')
@login_required
def my_games():
    games = g.user._get_current_object().get_games()
    return render_template('game/my_games.html', games = games)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=True, host='0.0.0.0', port=3030)
