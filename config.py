"""Flask configuration"""

class Config:
    """Base config."""
    # Define Folder with templates
    TEMPLATES_FOLDER = 'templates'
    # Define Track Mod SQL Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Define Secret Key
    SECRET_KEY = 'ed01997c4a2b400537bf2260a3593d04'


class ProdConfig(Config):
    # Chose env for server
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    # Database path
    SQLALCHEMY_DATABASE_URI = 'postgres://rklqhnwumcasxo:c9a8a9c132dc639ed63c5bb82fd0124f687b7a347ec6ea79b192be309e5bc84d@ec2-63-34-97-163.eu-west-1.compute.amazonaws.com:5432/ddhjl9a0su7cvc'


class DevConfig(Config):
     # Chose env for server
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    # Database path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Datenbank.db'

class TestConfig(Config):
     # Chose env for server
    TESTING = True
    DEBUG = True
    # Database path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Test.db'