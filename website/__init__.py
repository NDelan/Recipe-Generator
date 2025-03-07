from flask import Flask
from website.views import main_blueprint

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()