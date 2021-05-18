# __init__ 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
# deklariert die gesamte Appliaktion als Flask Applikation mit dem Namen __main__, falls sie aus diesem Skript gestartet wird
app = Flask(__name__)
# Konfiguration eines SecretKeys, mit welchem Daten beim Suer verschlüsslet werden, um Cross Site Script Angriffe zu verhindern
app.config['SECRET_KEY'] = 'ed01997c4a2b400537bf2260a3593d04'
# Konfiguration einer SQLITE Datenbankanbindung mit relativem Pfad von dieser Appliaktion aus
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LTApps.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
socketio = SocketIO(app)
from Tom_4328112 import routes
