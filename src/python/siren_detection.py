import time
import numpy as np
import pyaudio
import tensorflow_hub as hub
import requests
import csv
import cv2
import threading
import tensorflow as tf
from ultralytics import YOLO

# Suppress TensorFlow warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Load YAMNet model
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

# Load labels
def load_yamnet_labels():
    url = "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv"
    response = requests.get(url)
    labels = []
    if response.status_code == 200:
        decoded_content = response.content.decode("utf-8").splitlines()
        csv_reader = csv.reader(decoded_content)
        next(csv_reader)  # Skip header
        labels = [row[2] for row in csv_reader]
    return labels

class_labels = load_yamnet_labels()

# Shared flags
siren_detected_event = threading.Event()
ambulance_detected = False

# Siren detection function
def detect_siren():
    print("Listening for sirens")
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    while True:
        print("Capturing audio")
        frames = [stream.read(1024, exception_on_overflow=False) for _ in range(int(16000 / 1024 * 2))]

        waveform = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
        scores, _, _ = yamnet_model(waveform)
        class_scores = np.mean(scores, axis=0)
        top_class = np.argmax(class_scores)
        detected_class = class_labels[top_class] if top_class < len(class_labels) else "Unknown"

        print(f"Detected sound: {detected_class}")

        if "siren" in detected_class.lower() or "ambulance" in detected_class.lower():
            print("Siren detected")
            siren_detected_event.set()
        else:
            siren_detected_event.clear()

        time.sleep(1)

# Function to detect ambulance after siren
def detect_ambulance(model):
    global ambulance_detected

    while True:
        if siren_detected_event.is_set():
            print("checking for ambulance...")
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("❌ Camera not accessible.")
                time.sleep(2)
                continue

            start_time = time.time()
            detected = False

            while time.time() - start_time < 10:
                ret, frame = cap.read()
                if not ret:
                    print("⚠️ Frame capture failed.")
                    break

                results = model(frame)
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.cls)
                        class_name = model.names[class_id]
                        if "ambulance" in class_name.lower():
                            print("Ambulance detected. Turning lights GREEN.")
                            ambulance_detected = True
                            emergency_lights_on()
                            time.sleep(3)
                            ambulance_detected = False
                            detected = True
                            break
                    if detected:
                        break
                if detected:
                    break
                time.sleep(1)

            cap.release()
            cv2.destroyAllWindows()
        time.sleep(1)

# Emergency light control
def emergency_lights_on():

    print(" Emergency vehicle detected")
    time.sleep(10)

# Mock vehicle counting
def count_vehicles():
    return 5, 3

# Mock GPIO
def mock_gpio_output(pin, state):
    print(f"GPIO Pin {pin} set to {state}")

# Main traffic light control
def control_traffic_lights():
    while True:
        if ambulance_detected:
            time.sleep(1)
            continue

        c1, c2 = count_vehicles()
        d1, d2 = c1 * 2, c2 * 2
        print(f" Lane 1: {c1} vehicles,  Lane 2: {c2} vehicles")

        if c1 > c2:
            print("Green light on Lane 1.")
            mock_gpio_output(2, "LOW")
            mock_gpio_output(3, "HIGH")
            time.sleep(d1)
        else:
            print(" Green light on Lane 2.")
            mock_gpio_output(2, "HIGH")
            mock_gpio_output(3, "LOW")
            time.sleep(d2)

        time.sleep(0.5)

# Main execution
if _name_ == "_main_":
    model = YOLO("../main1.pt")  # Correct model path

    threading.Thread(target=detect_siren, daemon=True).start()
    threading.Thread(target=detect_ambulance, args=(model,), daemon=True).start()
    control_traffic_lights()