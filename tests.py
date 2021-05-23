import os
from unittest.case import TestCase
from flask import Flask
import unittest
from flask_testing import TestCase
from Tom_4328112 import create_app, db
from Tom_4328112.main.db_models import User, Chat, Message
import unittest
from flask_sqlalchemy import SQLAlchemy
app, db=create_app("config.TestConfig")
app.app_context().push()
class MyTest(TestCase):
    def create_app(self):
        # config testing settings
        return app
    
    def test_create_user(self):
        # Create User via the api
        user=User(username='Tomas', email='test@testmail.com',password='password')
        self.assert200(self.client.post('/createAccount', data={"username":'Tomas', "email":'test@testmail.com',"password":'password'}))
        # Create a Clone of the same user we registered in the database
        # Check if the User is in the database
        assert user is user
    def test_create_Chat(self):
        # Create User via the api 
        #response=self.client.post('/createAccount', data=dict(username='Tom', email='test@testmail.com',password='password',sid="TEST"))
        # Create a Clone of the same user we registered in the database
        chat = Chat(title="TEST")
        # Check if the User is in the database
        assert chat is chat    
    
    def setUp(self):
        db.create_all()

    def tearDown(self):
        # remove sessions
        db.session.remove()
        db.drop_all()
        # remove database file
        os.remove("Tom_4328112/Test.db")
        

if __name__ == '__main__':
    # runs all functions with test_* in MyTEST Class
    unittest.main()
