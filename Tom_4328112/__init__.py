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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://csxkuyiwuzeryk:dfc99d05f47b0cf76259f3abfed1e06dfc49c1cbe03ab0ddecfa572ddd46580a@ec2-63-34-97-163.eu-west-1.compute.amazonaws.com:5432/dbl4um2jdt8q85'
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
