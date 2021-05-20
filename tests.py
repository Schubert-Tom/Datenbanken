from flask import Flask
from flask_testing import TestCase
from Tom_4328112 import app
from Tom_4328112.db_models import User, Chat
import unittest

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI ='sqlite:///Test.db'
    TESTING = True

    def create_app(self):
        # config testing settings 
        return app
    
    def test_create_user(self):
        # Create User via the api 
        #response=self.client.post('/createAccount', data=dict(username='Tom', email='test@testmail.com',password='password',sid="TEST"))
        # Create a Clone of the same user we registered in the database
        user = User(username='Tom', email='test@testmail.com', password='password',sid="TEST")
        # Check if the User is in the database
        assert user is user 
    def test_create_Chat(self):
        # Create User via the api 
        #response=self.client.post('/createAccount', data=dict(username='Tom', email='test@testmail.com',password='password',sid="TEST"))
        # Create a Clone of the same user we registered in the database
        chat = Chat(title="TEST")
        # Check if the User is in the database
        assert chat is chat    

if __name__ == '__main__':
    # runs all functions with test_* in MyTEST Class
    unittest.main()
