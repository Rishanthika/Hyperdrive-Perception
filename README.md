# 🚀 Hyperdrive Perception

**KITTI-Trained YOLOv11n for Ultra-Low-Latency ADAS**

---

## 📌 Overview

Hyperdrive Perception is a real-time object detection system designed for **Advanced Driver Assistance Systems (ADAS)**. It uses a lightweight **YOLO-based model** trained on the **KITTI dataset** to detect road entities such as vehicles, pedestrians, and obstacles.

The system is optimized for **low latency and edge deployment**, enabling fast and reliable performance without relying on cloud infrastructure.

---

## 🎯 Features

* ⚡ Real-time object detection (~30 FPS)
* 🧠 Lightweight YOLO model (fast + efficient)
* 🚗 Detects cars, pedestrians, bicycles, trucks
* 📡 Vehicle-to-Vehicle (V2V) communication
* 📉 ONNX optimization for faster inference
* 🌐 Works offline (edge-based system)
* 📊 Hazard Urgency Score (HUS) for prioritization

---

## 🧠 System Architecture

### 🔄 Pipeline

1. Video Input (Camera / Video file)
2. Frame Preprocessing (resize, normalization)
3. YOLO Inference (object detection)
4. Distance & Velocity Estimation
5. Hazard Scoring (HUS calculation)
6. Data Transmission (TCP/UDP sockets)
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
| Processing      | NumPy              |

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

* **Severity** → importance of object (car, person, etc.)
* **Distance** → estimated from bounding box size
* **Velocity** → movement across frames

---

## 📂 Project Structure

```
Hyperdrive-Perception/
│── sender.py          # ONNX-based detection + UDP sender
│── server.py          # Detection + TCP communication
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

  * **TCP** → reliable communication, chat, stats
  * **UDP** → fast hazard transmission

---

## 📦 Dataset

This project uses the **KITTI Vision Benchmark Suite**, a standard dataset for autonomous driving and computer vision.

🔗 **Dataset Link:**
👉 [https://www.bing.com/search?q=kitti%20car%20dashcam%20dataset](https://www.bing.com/search?q=kitti%20car%20dashcam%20dataset)

### 📊 Dataset Details

* Captured using a **vehicle-mounted dashcam system**
* Includes real-world driving scenarios (urban, highways, rural)
* Object classes:

  * 🚗 Cars
  * 🚶 Pedestrians
  * 🚴 Cyclists
* Provides:

  * High-resolution images
  * 2D/3D bounding boxes
  * Sensor data (LiDAR, GPS)

### 💡 Why KITTI?

* Real-world complexity (lighting, occlusion, motion)
* Widely used benchmark dataset
* Ideal for ADAS and real-time perception systems

---

## ⚠️ Limitations

* Reduced accuracy for small/distant objects
* Sensitive to lighting and occlusion
* Dataset dependency affects generalization
* Lightweight model trades accuracy for speed

---

## 🔮 Future Enhancements

* Multi-object tracking
* Sensor fusion (LiDAR / Radar)
* Model pruning & quantization
* Deployment on embedded systems (Jetson, Raspberry Pi)
* Hardware acceleration (TensorRT)

---

## 🤝 Contributing

Contributions are welcome!
Fork the repo, create a branch, and submit a pull request.

---

## 📜 License

This project is intended for academic and research purposes.

---

## 👩‍💻 Author

**Rishanthika S**
Integrated M.Sc Data Science
Amrita Vishwa Vidyapeetham

