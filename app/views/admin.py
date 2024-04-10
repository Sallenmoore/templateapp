# Built-In Modules
import os
import shutil

# external Modules
from flask import Blueprint, get_template_attribute, render_template, request

from autonomous import log
from autonomous.auth import AutoAuth, auth_required

admin_page = Blueprint("admin", __name__)


@admin_page.route("/", methods=("GET",))
@auth_required()  # admin=True)
def index():
    return render_template("admin.html", context={"user": AutoAuth.current_user().pk})


@admin_page.route("/migration", methods=("POST",))
@auth_required()  # admin=True)
def migration():
    log("starting migration...")
    results = []
    log("...migration complete")

    return results


@admin_page.route("/dbdump", methods=("GET",))
# @auth_required()  # admin=True)
def dbdump():
    log("starting dump...")
    return f"<p>Success</p>"


@admin_page.route("/dbload", methods=("GET",))
# @auth_required()  # admin=True)
def dbload():
    log("starting load...")
    return f"<p>Success</p>"
