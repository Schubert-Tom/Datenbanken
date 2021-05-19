from flask import Flask
from Tom_4328112 import app

class MyTest(app):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app