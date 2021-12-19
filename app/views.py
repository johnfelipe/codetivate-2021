from datetime import datetime
from collections import deque
from time import sleep, time
import random
import os
import json
from .kbd import KBHit
import requests
# import pyaudio
# import wave 

from flask import session, request, redirect, render_template, Response
from dash.dependencies import State, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from fer import FER

from .config import *
from .secret import *

# audio = pyaudio.PyAudio()

from app import db, app, server, EMOTIONS
from app.forms import LoginForm
from app.hasher import hash_password
from app.hasher import verify_password_hash
from app.gen_graph import generate_figure, update_data, get_data
from app.fb import fetch_last

import cv2 as cv

HERE = os.path.dirname(__file__)
# detector = FER()
# print(">>> Ready! ")

# Initialize dashboard data:
# timestamp = deque(maxlen=20)
# angry = deque(maxlen=20)
# disgust = deque(maxlen=20)
# fear = deque(maxlen=20)
# happiness = deque(maxlen=20)
# sadness = deque(maxlen=20)
# surprise = deque(maxlen=20)
# neutral = deque(maxlen=20)
timestamp = []
angry = []
disgust = []
fear = []
happy = []
sad = []
surprise = []
neutral = []

for i in range(5):
    timestamp.append(str(datetime.now()))
    angry.append(random.random())
    disgust.append(random.random())
    fear.append(random.random())
    happy.append(random.random())
    sad.append(random.random())
    surprise.append(random.random())
    neutral.append(random.random())
    sleep(0.01)

initial_emo = {
    "timestamp": timestamp,
    "angry": angry,
    "disgust": disgust,
    "fear": fear,
    "happy": happy,
    "sad": sad,
    "surprise": surprise,
    "neutral": neutral
}

r = db.child("db").set(initial_emo)
# j = json.dumps(initial_emo)
# with open("firebase.json", "w") as f:
#     f.write(j)
#     f.close()

update_data(initial_emo)

# Create dash + Bootstrap components:
items = [
    dbc.DropdownMenuItem(
        children=["Patients"],
        href="/patients",
        external_link=True
    ),
    dbc.DropdownMenuItem(
        children=["About"],
        href="#",
        external_link=True,
        id="open"
    ),
    dbc.Modal([
        dbc.ModalHeader("About this project"),
        dbc.ModalBody(
            children=[
                dcc.Markdown(
                    """
                    #### General information

                    - **Patient:** John Doe
                    - **Since:** 09/09/2019
                    - **Last session:** 15/12/2019
                    - **Diagnosis:** schizophrenia
                    """
                )
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Close", id="close", className="ml-auto")
        ),
    ],
        id="modal",
        size="lg",
        scrollable=True
    ),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem(
        children=["Logout"],
        href="/login",
        external_link=True
    )
]

dropdowns = dbc.DropdownMenu(
    children=items,
    label="Menu",
    color="danger",
    right=True,
    className="nav-link btn btn-danger",
    nav=True,
    in_navbar=True,
    style={"text-decoration": "none", "padding": "0", "color": "#FFF"}
)

nav = dbc.Nav(
    children=[
        dbc.NavItem(
            children=[
                dbc.NavLink(
                    children=[
                        html.Img(
                            src="https://emojis.slackmojis.com/emojis/images/1450822151/257/github.png",
                            style={ "width": "15px" }
                        ),
                        " GitHub Repo"
                    ],
                    href="https://github.com/ozeliger/xed",
                    className="nav-link btn btn-light text-dark",
                    style={"margin-top": "9px"}
                )
            ],
            className="nav-item mr-sm-2"
        ),
        dbc.NavItem(
            children=[
                dbc.NavLink(
                    children=[
                        dropdowns
                    ],
                )
            ],
            className="nav-item dropdown my-2 my-sm-0",
            style={"text-decoration": "none", "padding": "0"}
        )
    ],
    className="navbar-nav navbar-expand-lg ml-auto flex-nowrap mt-3 mt-md-0",
    navbar=True
)

navbar = dbc.Navbar(
    children=[
        dbc.Container(
            children=[
                html.A(
                    # Use row and col to control vertical alignment of logo / brand:
                    dbc.Row(
                        children=[
                            dbc.Col(html.Img(src="../static/logo.png", height="45px")),
                            dbc.Col(dbc.NavbarBrand("Fusion Assistant", className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="/dashboard",
                    target="_parent"
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(nav, id="navbar-collapse", navbar=True)
            ]
        )
    ],
    color="dark",
    dark=True,
    className="navbar navbar-expand-lg navbar-dark bg-dark"
)

jumbotron = dbc.Container(
    children= [
        # html.H1("Webcam Test"),
        html.Img(src="/video_feed", style={ "width": "640px", "margin-left": "-100px"})
    ]
)

audio_button = dcc.Link(
    html.Button(
        "Record an Audio Session",
        id="audio-button"
    ),
    href="/audio-session"
)


# jumbotron = dbc.Container(
# 	children=[
# 		html.Br(),
# 		html.Br(),
# 		dbc.Jumbotron(
# 			children=[
# 				html.H1("Patient Record", className="display-4"),
# 				dcc.Markdown(
# 					"""
# 					#### General information

# 					- **Patient:** John Doe
# 					- **Since:** 01/12/2020
# 					- **Last session:** 15/05/2021
# 					- **Diagnosis:** Anxiety Disorder
# 					"""
# 				),
# 				html.P(
# 					"John has shown an altered perception of reality, "
# 					"including delusional thoughts, hallucinations, and "
# 					"disorganized speech and behaviour.",
# 					className="lead"
# 				),
# 				dbc.ButtonGroup(
# 					children=[
# 						dbc.Button(
# 							children=[
# 								html.A(
# 									children=["👥 Patient records"],
# 									href="/",
# 									target="_parent",
# 									style={"text-decoration": "none", "color": "#000"}
# 								)
# 							],
# 							color="light",
# 							className="md-auto text-light"
# 						),
# 						dbc.Button(
# 							children=[
# 								html.A(
# 									children=["📝 New record"],
# 									href="/",
# 									target="_parent",
# 									style={"text-decoration": "none", "color": "#FFF"}
# 								)
# 							],
# 							color="primary",
# 							className="md-auto text-dark"
# 						)
# 					],
# 				)
# 			]
# 		)
# 	]
# )

fig = generate_figure(initial_emo)

plot = dbc.Container(
    children=[
        html.Br(),
        html.Br(),
        dcc.Interval(id="timer", interval=1000),
        dcc.Graph(
            id="fer-graph",
            figure=fig,
            style={"padding-left": "100px"}
        ),
        html.Br(),
        html.Br(),
    ]
)

body = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[ jumbotron ],
                    md=5
                ),
                dbc.Col(
                    children=[ plot ],
                    md=7
                )
            ]
        ),
        dbc.Row(
            children=[
                audio_button
            ]
        )
    ]
)

# Create dash layout by adding components:
app.layout = html.Div([navbar, body])

# Add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Add callback for modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Add a callback to update plot
@app.callback(output=Output("fer-graph", "figure"),
              inputs=[Input("timer", "n_intervals")])
def update_graph(n_intervals):
    global EMOTIONS
    update_data(EMOTIONS)
    fig = generate_figure(EMOTIONS)
    return fig
    # global EMOTIONS
    # # EMOTIONS = update_data(EMOTIONS)
    # fig = generate_figure(EMOTIONS)
    # return fig

face_cascade_path = os.path.join(HERE, "cascades", "haarcascade_frontalface_default.xml")
face_cascade = cv.CascadeClassifier(face_cascade_path)

class VideoCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(0)

    def get_frame(self):
        return self.video.read()        
    
    def __del__(self):
        self.video.release()

# counter = 0
def gen(camera):
    # global counter

    while True:
        success, frame = camera.get_frame()
        if not success:
            print("Frame is None")
            break
        
        frame_copy = frame.copy()
        start_face_detection = time()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        # We select the most dominant face
        for (x, y, w, h) in faces:
            # face = cv.resize(frame[y:y + h, x:x + w], (48, 48))
            cv.rectangle(frame, (x - w // 32, y), (x + 33 * w // 32, y + 17 * h // 16), (0, 255, 0), 4)
            end_face_detection = time()
            delta_face = end_face_detection - start_face_detection
            # print(f"\n * Time for face {i} det.: {delta_face}")
            break
        
        # if counter % 15 == 0:
        #     output = detector.detect_emotions(frame_copy)
        #     if len(output) != 0:
        #         _ = update_data(get_data(output))
                
        # counter += 1
            
        ret, jpeg = cv.imencode(".jpg", cv.flip(frame, 1))
        jpeg = jpeg.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + jpeg + b"\r\n\r\n")

@server.route("/")
def index():
    # Base URL for app
    # Pop previous session:
    session.pop("user", None)
    return redirect("/login")

@server.route("/audio-session")
def audio_session():
    return render_template("audio-session.html")

@server.route("/dashboard")
def dashboard():
    # Patients URL for app.
    return render_template("dashboard.html")

@server.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera()), mimetype="multipart/x-mixed-replace; boundary=frame")

def read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

@server.route("/dashboardd", methods=["GET", "POST"])
def dashboardd():
    print("Uploading to AssemblyAI")
    # Get a temporary URL from Assembly AI
    upload_endpoint = "https://api.assemblyai.com/v2/upload"
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

    print("Uploading...")
    response = requests.post(
        upload_endpoint,
        headers={
            "authorization": ASSEMBLYAI_TOKEN,
        },
        data=read_file(WAVE_OUTPUT_FILENAME)
    )
    print("Uploaded!")

    json_payload = {
        "audio_url": response.json()["upload_url"],
        "sentiment_analysis": "true"
    }
    headers = {
        "authorization": ASSEMBLYAI_TOKEN,
        "content-type": "application/json",
    }

    response = requests.post(transcript_endpoint, json=json_payload, headers=headers)
    transcript_id = response.json()["id"]
    transcript_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    headers = {
        "authorization": ASSEMBLYAI_TOKEN,
    }

    while True:
        print("[INFO] Waiting for transcription to complete...")
        response = requests.get(transcript_endpoint, headers=headers)
        sleep(2)
        if response.json()["status"] in ["completed", "error"]:
            break
    print("Results have arrived!")

    # Get overall sentiment
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    sent = response.json()["sentiment_analysis_results"]
    if isinstance(sent, list):
        for para in sent:
            if para["sentiment"].lower() == "neutral":
                neutral_count += 1
            elif para["sentiment"].lower() == "positive":
                positive_count += 1
            elif para["sentiment"].lower() == "negative":
                negative_count += 1
        
        if neutral_count >= positive_count and neutral_count >= negative_count:
            LATEST_SENTIMENT = "Neutral"
        elif positive_count >= neutral_count and positive_count >= negative_count:
            LATEST_SENTIMENT = "Positive"
        else:
            LATEST_SENTIMENT = "Negative"
    else:
        LATEST_SENTIMENT = str(sent["sentiment"]).title()

    return render_template("dashboardd.html", LATEST_SENTIMENT=LATEST_SENTIMENT)

@server.route("/login", methods=["GET", "POST"])
def login():
    # Pop previous session:
    session.pop("user", None)

    # Create form:
    form = LoginForm(request.form)
    login_error = False

    if len(form.errors):
        print(form.errors)
    if request.method == "POST":
        user = form.user.data
        password = form.password.data
        if user == "jason" and password == "jason":
            session["user"] = user
            return redirect("/dashboard")
        else:
            login_error = True
    return render_template("login.html", login_error=login_error)
