"""Blogly application."""

from flask import Flask, request, redirect, render_template, session

from models import db, connect_db, User

from flask_debugtoolbar import DebugToolbarExtension

from forms import AddUserForm

import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
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
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)

