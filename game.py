from flask import Flask, g, render_template, flash, redirect, url_for
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user

import forms
import models

app = Flask(__name__)
app.secret_key = '1234567890'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user/login'
@login_manager.user_loader
def load_user(user_id):
    try:
        models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return render_template('index.html')

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




if __name__ == '__main__':
    models.initialize()
    app.run(debug=True, host='0.0.0.0', port=3030)
