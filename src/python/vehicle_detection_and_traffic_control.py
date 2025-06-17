import time
import numpy as np
import cv2
import math
import RPi.GPIO as GPIO
from ultralytics import YOLO
from sort import Sort

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in [2, 3, 4, 14, 15, 18, 17, 27]:
    GPIO.setup(pin, GPIO.OUT)

# YOLO setup
classNames = [
    "person", "bicycle", "car", "motorbike", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "N/A", "stop sign", "parking meter", "bench", "bird",
    "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "N/A",
    "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
    "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
    "chair", "couch", "potted plant", "bed", "dining table", "toilet", "N/A", "tv", "laptop",
    "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

# Use two video inputs or two cameras (adjust as needed)
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(0)  # Replace 2 with actual index or file for lane 2

cap1.set(3, 1280)
cap1.set(4, 720)
cap2.set(3, 1280)
cap2.set(4, 720)

model = YOLO("../yolo-weights/main1.pt")
tracker1 = Sort()
tracker2 = Sort()

def get_vehicle_counts(num_frames=10):
    ids1, ids2 = set(), set()
    for _ in range(num_frames):
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not ret1 or not ret2:
            continue

        results1 = model(frame1, stream=True)
        results2 = model(frame2, stream=True)

        def extract_detections(results):
            detections = np.empty((0, 5))
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    if classNames[cls] in ["car", "motorbike", "bus", "truck"]:
                        detections = np.vstack((detections, [x1, y1, x2, y2, conf]))
            return detections

        d1 = extract_detections(results1)
        d2 = extract_detections(results2)

        t1 = tracker1.update(d1)
        t2 = tracker2.update(d2)

        for obj in t1:
            ids1.add(int(obj[4]))
        for obj in t2:
            ids2.add(int(obj[4]))
        time.sleep(0.1)

    return len(ids1), len(ids2)

def lane_priority(c1, c2):
    if c1 == c2 and c1 != 0:
        return 1
    elif c1 == 0 and c2 == 0:
        return 0
    elif c1 > c2:
        return 1
    else:
        return 1

# MAIN LOOP
while True:
    c1, c2 = get_vehicle_counts()
    d1 = max(2, c1 * 2)
    d2 = max(2, c2 * 2)
    print(f"Initial Lane 1 count: {c1}, delay: {d1}")
    print(f"Initial Lane 2 count: {c2}, delay: {d2}")

    v = lane_priority(c1, c2)

    if v == 0:
        print("GREEN at lane 1 and 3 | RED at lane 4")
        GPIO.output(2, GPIO.LOW); GPIO.output(3, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW); GPIO.output(14, GPIO.LOW)
        GPIO.output(15, GPIO.LOW); GPIO.output(18, GPIO.HIGH)
        GPIO.output(17, GPIO.HIGH); GPIO.output(27, GPIO.HIGH)
        time.sleep(1)

    elif v == 1:
        print("PHASE 1: GREEN at lane 1 and 3")
        GPIO.output(2, GPIO.LOW); GPIO.output(3, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW); GPIO.output(14, GPIO.LOW)
        GPIO.output(15, GPIO.LOW); GPIO.output(18, GPIO.HIGH)
        GPIO.output(17, GPIO.HIGH); GPIO.output(27, GPIO.HIGH)
        time.sleep(5)

        print("PHASE 2: YELLOW at lane 1 and 3")
        GPIO.output(2, GPIO.HIGH); GPIO.output(3, GPIO.LOW)
        GPIO.output(4, GPIO.LOW); GPIO.output(15, GPIO.HIGH)
        GPIO.output(18, GPIO.LOW)
        time.sleep(2)

        print("PHASE 3: GREEN at lane 4")
        GPIO.output(2, GPIO.HIGH); GPIO.output(3, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW); GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)

        c1, _ = get_vehicle_counts()
        d1 = max(2, c1 * 2)
        print(f"Updated Lane 1 count: {c1}, delay: {d1}")
        time.sleep(d1)

        print("PHASE 4: YELLOW at lane 4")
        GPIO.output(27, GPIO.LOW)
        time.sleep(2)

        print("PHASE 5: GREEN at lane 1 and 2 | RED at 3 and 4")
        GPIO.output(2, GPIO.LOW); GPIO.output(3, GPIO.HIGH)
        GPIO.output(4, GPIO.LOW); GPIO.output(14, GPIO.HIGH)
        GPIO.output(15, GPIO.HIGH); GPIO.output(18, GPIO.HIGH)
        GPIO.output(17, GPIO.HIGH); GPIO.output(27, GPIO.HIGH)

        _, c2 = get_vehicle_counts()
        d2 = max(2, c2 * 2)
        print(f"Updated Lane 2 count: {c2}, delay: {d2}")
        time.sleep(d2)
