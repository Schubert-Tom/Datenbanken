# Run Server in Debug mode
from Tom_4328112 import create_app, socketio
app,db = create_app("config.DevConfig")
if __name__ == "__main__":
    socketio.run(app)
