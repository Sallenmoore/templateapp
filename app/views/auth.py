# Built-In Modules

# external Modules
import random
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, session, url_for

from autonomous import log
from autonomous.auth import AutoAuth, GithubAuth, GoogleAuth
from models.user import User
from models.world import World

auth_page = Blueprint("auth", __name__)


@auth_page.route("/login", methods=("GET", "POST"))
def login():
    log(AutoAuth.current_user())
    if AutoAuth.current_user() and AutoAuth.current_user().role != "guest":
        try:
            user = User.get(session["user"]["pk"])
        except Exception as e:
            return redirect(url_for("auth.logout"))
        if user and user.last_login:
            diff = datetime.now() - user.last_login
            if diff.days <= 30 and AutoAuth.current_user().state == "authenticated":
                return redirect(url_for("index.index"))

    if request.method == "POST":
        session["user"] = None
        if request.form.get("authprovider") == "google":
            authorizer = GoogleAuth()
            session["authprovider"] = "google"
        elif request.form.get("authprovider") == "github":
            authorizer = GithubAuth()
            session["authprovider"] = "github"
        uri, state = authorizer.authenticate()
        session["authprovider_state"] = state

        return redirect(uri)
    worlds = World.all()
    worlds = random.sample(worlds, k=min(4, len(worlds)))
    return render_template("login.html", context={}, worlds=worlds)


@auth_page.route("/authorize", methods=("GET", "POST"))
def authorize():
    if session["authprovider"] == "google":
        authorizer = GoogleAuth()
    elif session["authprovider"] == "github":
        authorizer = GithubAuth()
    response = str(request.url)
    # log(response)
    user_info, token = authorizer.handle_response(
        response, state=request.args.get("state")
    )
    user_info["provider"] = session["authprovider"]
    try:
        user = User.authenticate(user_info, token)
    except Exception as e:
        log(e, session["user"])
        session["user"] = None
    else:
        session["user"] = user.serialize()
    log(session["user"])
    return redirect(url_for("auth.login"))


@auth_page.route("/logout", methods=("POST", "GET"))
def logout():
    if session.get("user") and session["user"]["state"] != "guest":
        try:
            user = User.get(session["user"]["pk"])
            user.state = "unauthenticated"
            log(f"User {user} logged out")
            user.save()
        except Exception as e:
            log(e)
    session.pop("user")

    return redirect(url_for("auth.login"))
