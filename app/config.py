import uuid
import os


SECRET_KEY = uuid.uuid4().hex
DEBUG = True
JSON_SORT_KEYS = False

CHUNK_SIZE = 1024
# FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = os.path.join(os.path.dirname(__file__), "assets/output.wav")