# 🅿️ Smart Parking Availability System

A real-time parking management system using **Flask**, **OpenCV**, **MySQL**, and **Chart.js**.

---

## 🎯 Features

- **Vehicle Detection** – OpenCV adaptive thresholding for real-time occupancy detection
- **Slot Reservation** – Book parking slots with double-booking prevention
- **Overstay Detection** – Automatic alerting when vehicles exceed booking time
- **Admin Dashboard** – Live charts, occupancy analytics, and alert panels
- **Predictive Analytics** – Scikit-learn Linear Regression forecasts future availability
- **Demo Mode** – Runs without MySQL or a camera using simulated data

---

## 🏗 Folder Structure

```
smart_parking/
├── app.py                        # Flask application & API endpoints
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── detection/
│   ├── __init__.py
│   └── vehicle_detection.py      # OpenCV vehicle detector
├── prediction/
│   ├── __init__.py
│   └── forecasting.py            # Occupancy prediction (Linear Regression)
├── database/
│   └── models.sql                # MySQL schema & seed data
├── templates/
│   ├── index.html                # Main parking page
│   └── dashboard.html            # Admin dashboard
└── static/
    ├── css/
    │   └── style.css             # All styles
    └── js/
        ├── main.js               # Index page logic
        └── dashboard.js          # Dashboard logic & Chart.js
```

---

## ⚡ Step-by-Step Setup Guide

### Prerequisites

- **Python 3.9+** installed
- **MySQL 8.0+** installed and running (optional – app has demo fallback)
- **pip** package manager

### 1. Clone / Copy the Project

```bash
cd smart_parking
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database (Optional)

If you have MySQL running:

```bash
mysql -u root -p < database/models.sql
```

Or run the SQL manually in MySQL Workbench / phpMyAdmin.

> **Note:** If MySQL is not available, the app automatically falls back to demo/simulated data. All features still work.

### 5. Configure Environment Variables (Optional)

```bash
# Windows PowerShell
$env:DB_HOST = "localhost"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your_password"
$env:DB_NAME = "smart_parking"

# Linux / macOS
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=smart_parking
```

### 6. Run the Application

```bash
python app.py
```

The server starts at **http://localhost:5000**.

### 7. Open in Browser

| Page           | URL                            |
|----------------|--------------------------------|
| Parking View   | http://localhost:5000/          |
| Admin Dashboard| http://localhost:5000/dashboard |

---

## 🧠 API Endpoints

| Method | Endpoint          | Description                              |
|--------|-------------------|------------------------------------------|
| GET    | `/slots`          | Get all slot statuses                    |
| POST   | `/reserve`        | Reserve a slot (JSON body)               |
| GET    | `/dashboard-data` | Aggregated dashboard data                |
| GET    | `/predict?hours=6`| Predict occupancy for next N hours       |
| POST   | `/detect`         | Trigger a vehicle detection scan         |
| POST   | `/release/<id>`   | Release a slot and complete reservation  |

### Example – Reserve a Slot

```bash
curl -X POST http://localhost:5000/reserve \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Alice",
    "slot_id": 3,
    "start_time": "2026-03-02T10:00",
    "end_time": "2026-03-02T12:00"
  }'
```

---

## 📌 Notes

- The system works in **demo mode** without MySQL or a camera.
- To use real vehicle detection, provide a video file or webcam:
  ```bash
  set VIDEO_SOURCE=parking_feed.mp4
  python app.py
  ```
- OpenCV processes video frames directly for vehicle detection.
- For academic projects, the simulation mode provides realistic behaviour out of the box.
