Here’s a **complete, polished GitHub README.md** for your project 👇

---

# 🚀 Hyperdrive Perception

**KITTI-Trained YOLOv11n for Ultra-Low-Latency ADAS**

---

## 📌 Overview

Hyperdrive Perception is a real-time object detection system designed for **Advanced Driver Assistance Systems (ADAS)**. It uses a lightweight **YOLO-based model** trained on the **KITTI dataset** to detect road entities such as vehicles, pedestrians, and obstacles.

The system is optimized for **low latency and edge deployment**, enabling fast decision-making without relying on cloud infrastructure.

---

## 🎯 Features

* ⚡ Real-time object detection (~30 FPS)
* 🧠 Lightweight YOLO model (fast + efficient)
* 🚗 Detects cars, pedestrians, bicycles, trucks
* 📡 Vehicle-to-vehicle (V2V) communication support
* 📉 ONNX optimization for faster inference
* 🌐 Works offline (edge-based system)
* 📊 Hazard scoring using HUS (Hazard Urgency Score)

---

## 🧠 System Architecture

### 🔄 Pipeline

1. Video Input (Camera / Video file)
2. Frame Preprocessing (resize, normalize)
3. YOLO Inference (object detection)
4. Distance & Velocity Estimation
5. Hazard Scoring (HUS calculation)
6. Data Transmission (Socket/UDP)
7. Real-time Visualization

---

## ⚙️ Tech Stack

| Category        | Tools / Libraries  |
| --------------- | ------------------ |
| Language        | Python             |
| Deep Learning   | Ultralytics YOLO   |
| Computer Vision | OpenCV             |
| Optimization    | ONNX, ONNX Runtime |
| Networking      | Socket (TCP/UDP)   |
| Math/Processing | NumPy              |

---

## 📊 Performance

| Metric    | Value     |
| --------- | --------- |
| FPS       | ~30 FPS   |
| mAP@0.5   | ~0.85     |
| Precision | ~0.70     |
| Recall    | ~0.65     |
| Inference | ~30–35 ms |

---

## 🧮 Hazard Urgency Score (HUS)

The system prioritizes detected objects using:

```
HUS = α * Severity + β * (1 / Distance) + γ * Velocity
```

* Severity → object importance (car, person, etc.)
* Distance → estimated from bounding box
* Velocity → object movement between frames

---

## 📂 Project Structure

```
Hyperdrive-Perception/
│── sender.py          # ONNX-based detection + UDP sender
│── server.py          # Detection + TCP client + stats
│── requirements.txt
│── README.md
│── weights/           # Model weights (.pt / .onnx)
│── assets/            # Sample videos/images
```

---

## 🛠️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/hyperdrive-perception.git
cd hyperdrive-perception
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Run Sender (ONNX + UDP)

```bash
python sender.py
```

### Run Client (Detection + TCP)

```bash
python server.py
```

---

## 🌐 Networking

* Supports **real-time communication between vehicles**
* Uses:

  * TCP (for reliability + chat + stats)
  * UDP (for fast hazard transmission)

---

## 📦 Dataset

* KITTI Vision Benchmark Suite
* Contains real-world driving scenarios
* Classes: cars, pedestrians, cyclists, etc.

---

## ⚠️ Limitations

* Reduced accuracy for small or distant objects
* Sensitive to lighting and occlusions
* Depends on dataset diversity
* Lightweight model trades some accuracy for speed

---

## 🔮 Future Enhancements

* Multi-object tracking
* Sensor fusion (LiDAR / Radar)
* Model quantization & pruning
* Deployment on Raspberry Pi / Jetson
* Edge-AI acceleration (TensorRT)

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo, create a branch, and submit a PR.

---

## 📜 License

This project is for academic and research purposes.

---

## 👩‍💻 Author

**Rishanthika S**
Integrated M.Sc Data Science
Amrita Vishwa Vidyapeetham

s

