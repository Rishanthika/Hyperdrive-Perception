import cv2
import time
import json
import socket
import numpy as np
from ultralytics import YOLO
from queue import PriorityQueue
import threading

# ==============================
# NETWORK CONFIG
# ==============================
RECEIVER_IP = "192.168.137.89"   # change if using different PC
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ==============================
# LOAD ONNX MODEL (UPDATED)
# ==============================
model = YOLO(r"D:\Final Year Project\deeplearning Model\yolo_kitti_dashcam\yolov8n_kitti_dashcam5\weights\best.onnx" , task="detect")

# ==============================
# PARAMETERS
# ==============================
ALPHA, BETA, GAMMA = 0.5, 0.3, 0.2

severity_map = {
    "person": 1.0,
    "car": 0.8,
    "truck": 0.9,
    "bicycle": 0.7,
    "motorbike": 0.8
}

pq = PriorityQueue()
prev_positions = {}

# ==============================
# CHAT THREAD
# ==============================
def chat_sender():
    while True:
        msg = input("You (Sender): ")
        packet = {
            "type": "chat",
            "message": msg,
            "time": time.time()
        }
        sock.sendto(json.dumps(packet).encode(), (RECEIVER_IP, PORT))

threading.Thread(target=chat_sender, daemon=True).start()

# ==============================
# FUNCTIONS
# ==============================
def estimate_distance(h):
    return max(1, 1000 / h)

def compute_hus(s, d, v):
    return ALPHA*s + BETA*(1/d) + GAMMA*v

# ==============================
# VIDEO
# ==============================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Improve FPS
    frame = cv2.resize(frame, (640, 480))

    # ONNX inference with confidence threshold
    results = model(frame, conf=0.4)

    current_positions = {}

    for r in results:
        for box, cls in zip(r.boxes.xyxy, r.boxes.cls):

            x1, y1, x2, y2 = map(int, box)
            label = model.names[int(cls)]

            if label not in severity_map:
                continue

            severity = severity_map[label]

            h = y2 - y1
            distance = estimate_distance(h)

            center = ((x1+x2)//2, (y1+y2)//2)
            current_positions[label] = center

            velocity = 0
            if label in prev_positions:
                velocity = np.linalg.norm(
                    np.array(center) - np.array(prev_positions[label])
                )

            hus = compute_hus(severity, distance, velocity)

            packet = {
                "type": "hazard",
                "vehicle_id": "V1",
                "hazard": label,
                "severity": severity,
                "distance": round(distance, 2),
                "velocity": round(velocity, 2),
                "HUS": round(hus, 3),
                "time": time.time()
            }

            pq.put((-hus, packet))

            # DRAW BOX
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame,
                        f"{label} HUS:{round(hus,2)}",
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,(0,255,0),2)

    prev_positions = current_positions

    # ==============================
    # SEND PRIORITY PACKETS
    # ==============================
    while not pq.empty():
        _, pkt = pq.get()
        sock.sendto(json.dumps(pkt).encode(), (RECEIVER_IP, PORT))
        print("[SENT]", pkt)

    cv2.imshow("Sender - ONNX Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()