import os

from config import Config
from flask import Flask, url_for
from views import index

from autonomous import log
from autonomous.auth import AutoAuth
from filters.model import defined
from models.user import User


def create_app():
    app = Flask(os.getenv("APP_NAME", __name__))
    app.config.from_object(Config)

    #################################################################
    #                                                        Plug-ins                                      #
    #################################################################

    AutoAuth.user_class = User
    # Configure Filters
    app.jinja_env.filters["defined"] = defined
    if app.config["DEBUG"]:
        app.jinja_env.add_extension("jinja2.ext.debug")

    ######################################
    #              Routes                #
    ######################################
    @app.route("/favicon.ico")
    def favicon():
        return url_for("static", filename="images/favicon.ico")

    @app.route("/docs", endpoint="docs", methods=("GET", "POST"))
    def docs():
        return {"redirect": os.environ.get("DOC_URL", "#")}

    ######################################
    #           Blueprints               #
    ######################################

    app.register_blueprint(index.index_endpoint, url_prefix="/")

    return app
