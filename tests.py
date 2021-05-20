from flask import Flask
from flask_testing import TestCase
from Tom_4328112 import app,db
from Tom_4328112.db_models import *
import unittest

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI ='sqlite:///Test.db'
    TESTING = True

    def create_app(self):
        # config testing settings 
        app.config['TESTING'] = True
        return app
    
    def test_create_user(self):
        #user = User()
        #db.session.add(user)
        #db.session.commit()

        # this works
        #assert user in db.session

        response = self.client.get("/")

        # this raises an AssertionError
        #assert user in db.session
        pass
    
    def setUp(self):
        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    # runs all functions with test_* in MyTEST Class
    unittest.main()
