# Run Derver in Production Mode
from Tom_4328112 import create_app, socketio
app, db = create_app("config.ProdConfig")
if __name__ == "__main__":
    socketio.run(app)
