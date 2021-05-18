# __init__ 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
# Select Environment dev or prod
ENV ='dev'
# deklariert die gesamte Appliaktion als Flask Applikation mit dem Namen __main__, falls sie aus diesem Skript gestartet wird
app = Flask(__name__)
if ENV =='dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LTApps.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mksxavarujfwmi:25e05328a54d17914a2cd1a231d29ac0e942a3dd7411213701178fa7441255ef@ec2-54-163-254-204.compute-1.amazonaws.com:5432/d562uvts2a0r57'
# Konfiguration eines SecretKeys, mit welchem Daten beim Suer verschlüsslet werden, um Cross Site Script Angriffe zu verhindern
app.config['SECRET_KEY'] = 'ed01997c4a2b400537bf2260a3593d04'
# Konfiguration einer SQLITE Datenbankanbindung mit relativem Pfad von dieser Appliaktion aus
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///LTApps.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
socketio = SocketIO(app)
from Tom_4328112 import routes
