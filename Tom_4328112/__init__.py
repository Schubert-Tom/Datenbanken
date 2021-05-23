from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
# Select Environment dev or prod
# deklariert die gesamte Appliaktion als Flask Applikation mit dem Namen __main__, falls sie aus diesem Skript gestartet wird
socketio = SocketIO()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager= LoginManager()

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    # INIT main blueprint for all routes and events in /main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # INIT extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    login_manager.login_view = "main.login"
    login_manager.login_message_category = "info"
    return app , db
