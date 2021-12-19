from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc
import pyrebase

# Connect to Firebase:
config = {}
config = firebaseConfig = {
    "apiKey": "AIzaSyB0z9TUAJy3dxgKSnpbLm1eyjC0MM4jS0k",
    "authDomain": "cascade-ed906.firebaseapp.com",
    "databaseURL": "https://cascade-ed906-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "cascade-ed906",
    "storageBucket": "cascade-ed906.appspot.com",
    "messagingSenderId": "584236177035",
    "appId": "1:584236177035:web:0ecbb9d71ef0bdd4ebe68e"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Create a Flask server:
server = Flask(__name__)
server.config.from_pyfile("config.py")

# Create a Dash app:
app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix="/session/",
        external_stylesheets=[dbc.themes.LUX]
    )

EMOTIONS = {
	"timestamp": [],
	"angry": [],
	"disgust": [],
	"fear": [],
	"happy": [],
	"sad": [],
	"surprise": [],
	"neutral": [],
}

if __name__ == "__main__":
    from views import *
    app.run_server(debug=True, threaded=True)
