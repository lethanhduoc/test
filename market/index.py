from flask import render_template, request, redirect, url_for, flash
from os import path
from flask_login import login_user



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babelex import Babel
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = '#$%^456dssfdfdad$#'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:16102311@localhost/bullapp?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)# truyen tham so

bcrypt = Bcrypt(app)
babel = Babel(app=app)
login = LoginManager(app=app)


from market.admin import *
from market.forms import RegisterForm, LoginForm
from market.models import Product, User
import market.utils as utils

@app.route("/homesssss")
def app_homessss():
    users = [{
        "name": "nguyen van a",
        "email": "123@gmail.com"}, {
        "name": "nguyen van b",
        "email": "456@gmail.com"}, {
        "name": "nguyen van c",
        "email": "789@gmail.com"
    }]
    kw = request.args.get("keyword")
    if kw:
        users = [u for u in users if u['name'].lower().find(kw.lower()) >= 0]
        # kq = []
    # for u in users:
    # if u['name'].find(kw) >= 0:
    # kq.append(u)
    # users = kq

    return render_template('base.html', user=users)


@app.route('/admin-login', methods=['POST', 'GET'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              name=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template("dangky.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.name}', category='success')
            return redirect(url_for('home'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home"))


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)