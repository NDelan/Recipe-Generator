"""
This module initializes the Flask application and registers blueprints.
"""

from flask import Flask
from .views import main_blueprint

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    create_app()
