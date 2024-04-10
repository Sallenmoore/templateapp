"""
app.py - Flask Application Factory

This module defines a Flask application factory for creating the main application
object. It configures various components, such as routes, blueprints, and extensions.

Usage:
1. Import the create_app function.
2. Call create_app() to create the Flask app object.

Example:
    app = create_app()

Attributes:
    - Config: A configuration class defining application-wide settings.
    - index_page: Blueprint for the main index page.
    - auth_page: Blueprint for authentication-related pages.
    - admin_page: Blueprint for admin-related pages.
    - region_page: Blueprint for region-related pages.
    - city_page: Blueprint for city-related pages.
    - location_page: Blueprint for location-related pages.
    - faction_page: Blueprint for faction-related pages.
    - character_page: Blueprint for character-related pages.
    - item_page: Blueprint for item-related pages.
    - encounter_page: Blueprint for encounter-related pages.
    - creature_page: Blueprint for creature-related pages.

Functions:
    - create_app: Function to create and configure the Flask app object.

Routes:
    - /favicon.ico: Endpoint to serve the favicon.

Blueprints:
    - The blueprints are registered with the app object, each with its respective
      URL prefix.

Extensions:
    - TBD

Configurations:
    - The app is configured using settings from the Config class.

Note:
    Make sure to set the APP_NAME environment variable to specify the Flask app's name.

"""

import os

from config import Config
from filters.model import defined
from flask import Flask, url_for
from models.user import User
from views.admin import admin_page
from views.auth import auth_page
from views.index import index_page

from autonomous import log
from autonomous.auth import AutoAuth


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask app object.
    """
    app = Flask(os.getenv("APP_NAME", __name__))
    app.config.from_object(Config)

    # Configure Extensions
    if app.config["DEBUG"]:
        app.jinja_env.add_extension("jinja2.ext.debug")

    # Configure Filters
    app.jinja_env.filters["defined"] = defined
    AutoAuth.user_class = User

    # Configure Routes
    @app.route("/favicon.ico")
    def favicon():
        """Endpoint to serve the favicon."""
        return url_for("static", filename="images/favicon.ico")

    # Register Blueprints
    app.register_blueprint(index_page)
    app.register_blueprint(auth_page, url_prefix="/auth")
    app.register_blueprint(admin_page, url_prefix="/admin")

    return app
