from LTHome import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import Blueprint 




# Creating new database
# from LTHome import *
# from LTHome.db_models import *
# db.create_all()



# To get the extension login_manager running need some functions --> Usermixin and this decorater
# Usermixin is a class to replace the four functions:
#   # isauthenticated()
#   # isactive()
#   # isanonymous()
#   # getid()
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) # Zieht den User aus der Datenbank
    # Dieser User der hier returnt wird muss die oben genannten Methoden implementieren
    # Dazu wurde das UserMixin als Parent mitgewählt --> Mehrfachvererbung

link = db.Table('link',
                db.Column('user', db.Integer, db.ForeignKey('user.id')),
                db.Column('chat', db.Integer, db.ForeignKey('chat.chat_id'))
                )


# The db File gets created locally with the commands:
# from server import db
# db.create_all()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    sid=db.Column(db.String(60),unique=True)
    # Creates a relationship to the other class Chat, This relationship isnt a column in the table
    # Its just a relationship defined in the class which creates a query getting executed from sql alchemy in iterating over data.
    # lazy True means that the query gets loaded in one rush
    chats = db.relationship('Chat', secondary=link, backref=db.backref('chat_participants', lazy='dynamic'))

    def __repr__(self):
        # Method defines how object get printet out  
        return f"User('{self.username}','{self.email}')"


class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    messages = db.relationship('Message', backref='chat_room', lazy=True)
    def __repr__(self):
        return f"{self.title}"


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), nullable=False)
    user_name=db.Column(db.String(20), nullable=False)

    def __repr__(self):
        #  Method defines how object get printet out
        return f"Message:'{self.text}','{self.date}' in Room '{self.chat}')"

    # The classes are Tables with columns
    # If you want to acces stored data u should use the classes and query over them with filters.

# This module is creating a database scema and all relevant components and KEys of the tables.
# In the creation we've got 1 * n realtionships, 1*1, n*n.
# The 1*n is created with a db.relationship function which creates a connection.
# It kinda creates a imagniary column in the database mentioned in the function.
# With this query its possible to iterate about i.e all messages which refer to the same Chat.
# This List of n sets is stored in i.e. messages

# The n*n relationship has to work with an association table
# In this case we havent got an Foreign Key which refers back to table initiating the relationship like we got in the 1*n relationship
# In this case it refers to the association table which stores to foreign keys for both tables.
# So with the call secondary= association_table (i.e:link) it instantiates a query to the table which connects to n Chats and thats possible for n Users
# --> n*n
#
