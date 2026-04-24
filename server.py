import socket
import threading
import time
import statistics
import json
from datetime import datetime
import cv2
import numpy as np
from ultralytics import YOLO

# --- Configuration ---
host = "10.176.224.188"   # Server IP
port = 12345

# --- YOLO MODEL ---
model = YOLO(r"D:\Final Year Project\deeplearning Model\yolo_kitti_dashcam\yolov8n_kitti_dashcam5\weights\best.pt")

# --- Parameters ---
ALPHA, BETA, GAMMA = 0.5, 0.3, 0.2

severity_map = {
    "person": 1.0,
    "car": 0.8,
    "truck": 0.9,
    "bicycle": 0.7
}

# --- Global Variables ---
bytes_sent = 0
rtt_history = []
stop_event = threading.Event()

# -----------------------------
# FUNCTIONS
# -----------------------------

def compute_hus(s, d, v):
    return ALPHA*s + BETA*(1/d) + GAMMA*v

def estimate_distance(h):
    return max(1, 1000/h)

def measure_latency(sock, trials=5):
    rtts = []
    for i in range(trials):
        msg = json.dumps({"type": "ping", "time": time.time()}).encode()
        start = time.time()
        sock.send(msg)
        echo = sock.recv(1024)
        end = time.time()
        rtts.append((end - start) * 1000)
    return rtts

def display_stats():
    elapsed = time.time() - start_time
    throughput = (bytes_sent * 8) / (elapsed * 1000) if elapsed > 0 else 0
    avg_ping = sum(rtt_history)/len(rtt_history) if rtt_history else 0
    jitter = statistics.pstdev(rtt_history) if len(rtt_history)>1 else 0

    print("\n" + "━"*50)
    print(f"📊 CLIENT STATS | {datetime.now().strftime('%H:%M:%S')}")
    print(f"🔹 Latency   : {avg_ping:.2f} ms")
    print(f"🔹 Jitter    : {jitter:.2f} ms")
    print(f"🔹 Throughput: {throughput:.2f} kbps")
    print("━"*50 + "\n")

# -----------------------------
# RECEIVE THREAD
# -----------------------------
def receive_messages(sock):
    global bytes_sent

    while not stop_event.is_set():
        try:
            data = sock.recv(1024)

            if not data:
                print("❌ Server disconnected")
                stop_event.set()
                break

            bytes_sent += len(data)

            try:
                pkt = json.loads(data.decode())
            except:
                continue

            if pkt["type"] == "chat":
                print(f"\n💬 [Server]: {pkt['message']}")

            elif pkt["type"] == "ping":
                sock.send(data)

            display_stats()

        except:
            stop_event.set()
            break

# -----------------------------
# CONNECT
# -----------------------------
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
except:
    print("❌ Connection failed")
    exit()

print(f"✅ Connected to server {host}:{port}")

start_time = time.time()
rtt_history = measure_latency(client_socket)
display_stats()

threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

# -----------------------------
# VIDEO INPUT (UPDATED ✅)
# -----------------------------
cap = cv2.VideoCapture(r"C:\Users\VIGNESH\Downloads\13588857_3840_2160_30fps.mp4")

prev_positions = {}

# -----------------------------
# YOLO DETECTION LOOP
# -----------------------------
while not stop_event.is_set():
    ret, frame = cap.read()

    if not ret:
        print("✅ Video ended")
        break

    # 🔥 PERFORMANCE FIX
    frame = cv2.resize(frame, (640, 480))

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
                "vehicle_id": "Client_Vehicle",
                "hazard": label,
                "distance": round(distance,2),
                "HUS": round(hus,3),
                "time": time.time()
            }

            try:
                client_socket.send(json.dumps(packet).encode())
                print(f"[SENT] {label} | HUS={round(hus,2)}")
            except:
                stop_event.set()
                break

    prev_positions = current_positions

# -----------------------------
# CLEANUP
# -----------------------------
cap.release()
client_socket.close()
stop_event.set()