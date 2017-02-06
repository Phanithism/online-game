from flask import Flask, g, render_template, flash, redirect, url_for
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import forms
import models

app = Flask(__name__)
app.secret_key = '1234567890'

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


@app.route('/new_game', methods = ['GET', 'POST'])
@login_required
def new_game():
    form = forms.GameForm()
    if form.validate_on_submit():
        models.Game.create(
                    name = form.name.data, description = form.description.data,
                    logo = form.logo.data, embed_url = form.embed_url.data,
                    user = g.user._get_current_object()
                    )
        flash("successfully added a game", 'notice')
        return redirect(url_for('index'))
    else:
        return render_template('game/new_game.html', form = form)

@app.route('/game/<name>')
def game(name = None):
    game = models.Game.get(models.Game.name == name)
    return render_template('game/game.html', game = game)



if __name__ == '__main__':
    models.initialize()
    app.run(debug=True, host='0.0.0.0', port=3030)
