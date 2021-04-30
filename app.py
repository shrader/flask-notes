"""Blogly application."""

from flask import Flask, request, redirect, render_template, session

from models import db, connect_db, User

from flask_debugtoolbar import DebugToolbarExtension

from forms import AddUserForm, LoginUserForm

import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
#SECRET KEY should obviously be changed and not included in the source code if you intend on deploying
app.config['SECRET_KEY'] = "SECRET!" 
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/")
def home():
    """ redirect to the register page"""
  
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    form = AddUserForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        first_name =form.first_name.data
        last_name =form.last_name.data
        email =form.email.data
        #username, pwd, first_name, last_name, email

        user = User.register(name, pwd, first_name, last_name, email)
        db.session.add(user)
        db.session.commit()

        session["user_name"] = name

        # on successful login, redirect to secret page
        return redirect(f"/user/{user.name}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user."""

    form = LoginUserForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name, pwd)
        session["user_name"] = user.username

        # on successful login, redirect to secret page
        return redirect(f"/users/{user.username}")

    else:
        return render_template("login.html", form=form)


@app.route("/secret")
def secret():
    """Display the secret page"""
  
    return render_template("secret.html")

@app.route("/users/<username>")
def user_page(username):
    """Display the user page for logged-in users"""
    if session["user_name"] == username:

        user = User.query.filter_by(username=username ).first()

        return render_template("display_user.html", user = user)

