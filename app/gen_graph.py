import numpy as np
import random
from app import db, EMOTIONS
from app.fb import fetch_last
from datetime import datetime
import json

# from pprint import pprint
import gc 
from time import time 

# def update_data(emotions_dict):
# 	# latest_data = fetch_last(db, "db")
# 	# latest_data = [entry.val() for entry in latest_data.each()]
# 	latest_data = json.load(open("firebase.json"))
# 	# print("This is latest data")
# 	# print(latest_data)

# 	emotions = {
# 		"angry": [],
# 		"disgust": [],
# 		"fear": [],
# 		"happy": [],
# 		"neutral": [],
# 		"sad": [],
# 		"surprise": [],
# 		"timestamp": [],
# 	}

# 	for i in range(len(latest_data["angry"])):
# 		emotions["angry"].append(latest_data["angry"][i])
# 		emotions["disgust"].append(latest_data["disgust"][i])
# 		emotions["fear"].append(latest_data["fear"][i])
# 		emotions["happy"].append(latest_data["happy"][i])
# 		emotions["neutral"].append(latest_data["neutral"][i])
# 		emotions["sad"].append(latest_data["sad"][i])
# 		emotions["surprise"].append(latest_data["surprise"][i])
# 		emotions["timestamp"].append(latest_data["timestamp"][i])
	
# 	if isinstance(emotions_dict, dict) and emotions_dict != {}:
# 		# print("Oh no!")
# 		emotions["timestamp"].append(emotions_dict["timestamp"])
# 		emotions["angry"].append(emotions_dict["angry"])
# 		emotions["disgust"].append(emotions_dict["disgust"])
# 		emotions["fear"].append(emotions_dict["fear"])
# 		emotions["happy"].append(emotions_dict["happy"])
# 		emotions["sad"].append(emotions_dict["sad"])
# 		emotions["surprise"].append(emotions_dict["surprise"])
# 		emotions["neutral"].append(emotions_dict["neutral"])

# 		# # Push
# 		# r = db.child("db").set(emotions)
# 		j = json.dumps(emotions)
# 		with open("firebase.json", "w") as f:
# 			f.write(j)
# 			f.close()

# 	return emotions

	# if len(latest_data["angry"]) != 0:
	# 	global EMOTIONS
	# 	EMOTIONS["timestamp"].append(datetime.now())
	# 	EMOTIONS["angry"].append(latest_data["angry"])
	# 	EMOTIONS["disgust"].append(latest_data["disgust"])
	# 	EMOTIONS["fear"].append(latest_data["fear"])
	# 	EMOTIONS["happy"].append(latest_data["happy"])
	# 	EMOTIONS["sad"].append(latest_data["sad"])
	# 	EMOTIONS["surprise"].append(latest_data["surprise"])
	# 	EMOTIONS["neutral"].append(latest_data["neutral"])

	# # 	return EMOTIONS
	# global EMOTIONS
	# EMOTIONS["timestamp"].append(datetime.now())
	# EMOTIONS["angry"].append(random.uniform(0.0, 0.2))
	# EMOTIONS["disgust"].append(random.uniform(0.0, 0.2))
	# EMOTIONS["fear"].append(random.uniform(0.0, 0.2))
	# EMOTIONS["happy"].append(random.uniform(0.6, 1.0))
	# EMOTIONS["sad"].append(random.uniform(0.0, 0.2))
	# EMOTIONS["surprise"].append(random.uniform(0.3, 0.5))
	# EMOTIONS["neutral"].append(random.uniform(0.3, 0.6))
	# return

def update_data(emotions):
	global EMOTIONS
	EMOTIONS["timestamp"].append(datetime.now())
	EMOTIONS["angry"].append(random.uniform(0.0, 0.2))
	EMOTIONS["disgust"].append(random.uniform(0.0, 0.2))
	EMOTIONS["fear"].append(random.uniform(0.0, 0.2))
	EMOTIONS["happy"].append(random.uniform(0.6, 1.0))
	EMOTIONS["sad"].append(random.uniform(0.0, 0.2))
	EMOTIONS["surprise"].append(random.uniform(0.3, 0.5))
	EMOTIONS["neutral"].append(random.uniform(0.3, 0.6))
	return

def get_data(output):
	# print("\n\n\n\nThis is output ", output, "\n\n\n\n")
	return {
		"timestamp": str(datetime.now()),
		"angry": float(output[0]["emotions"]["angry"]),
		"disgust": float(output[0]["emotions"]["disgust"]),
		"fear": float(output[0]["emotions"]["fear"]),
		"happy": float(output[0]["emotions"]["happy"]),
		"sad": float(output[0]["emotions"]["sad"]),
		"surprise": float(output[0]["emotions"]["surprise"]),
		"neutral": float(output[0]["emotions"]["neutral"]),
	}

def generate_figure(emotions):
	return {
		"data": [
			dict(
				x=np.array(emotions["timestamp"]),
				y=np.array(emotions[key]),
				name=f"{key}",
				# marker=dict(
				# 	color="rgb(55, 83, 109)"
				# ),
				line=dict(
					shape="spline"
				)
			) for key in emotions.keys() if key != "timestamp"
		],
		"layout": dict(
			title="Emotion Activation",
			showlegend=True,
			legend=dict(
				x=0,
				y=1.0
			),
			margin=dict(l=40, r=0, t=40, b=30)
		)
	}