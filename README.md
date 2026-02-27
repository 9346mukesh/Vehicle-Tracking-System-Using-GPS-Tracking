# RideShare Pro: GPS-Based Vehicle Tracking System with ML-Enhanced Route Prediction 🚗

RideShare Pro is a full-stack, real-time vehicle tracking and ride-sharing platform powered by **Machine Learning** models for ETA prediction, dynamic fare estimation, and smart driver–passenger matching. Built with **Flask**, **SQLAlchemy**, **Socket.IO**, and trained on the **Porto Taxi Trajectory** dataset, it delivers role-based dashboards for customers, drivers, and administrators with live GPS simulation across **Bangalore** and **Porto** cities.

---

## 🌟 Features

- **Real-Time GPS Tracking:** Live vehicle location streaming via WebSocket (Socket.IO) with Leaflet.js maps.
- **ML-Powered ETA Prediction:** XGBoost and Random Forest models trained on 100k+ taxi trajectories predict trip durations accurately.
- **Dynamic Fare Estimation:** Time-of-day surge pricing with city-specific base fares and per-km rates.
- **Role-Based Dashboards:** Dedicated interfaces for Customers, Drivers, and Admins with access control.
- **Voice Assistant:** Hands-free ride booking and navigation using the Web Speech API.
- **K-Means Clustering:** Start and end point clustering for smart driver matching and demand pattern analysis.
- **Multi-City Support:** Pre-configured city maps for Bangalore (India) and Porto (Portugal).
- **Analytics Dashboard:** Interactive charts (Chart.js) for trip distribution, speed analysis, and hourly demand trends.
- **Real-Time Notifications:** Instant ride request alerts and status updates via WebSocket.

---

## 🎯 Objectives

1. **Accurate ETA Prediction** — Leverage XGBoost regression trained on GPS polyline features (distance, bearing, straightness) and temporal features (hour, day, rush-hour flags).
2. **Dynamic Pricing** — Automatically adjust fares based on distance, time-of-day, and traffic conditions (rush hour, late night).
3. **Real-Time Fleet Monitoring** — Simulate and track 10+ vehicles with continuous GPS coordinate updates on interactive maps.
4. **Smart Driver Matching** — Use K-Means spatial clustering (150 start clusters, 180 end clusters) to match nearby drivers to ride requests.
5. **Scalable Architecture** — Modular Flask application with SQLAlchemy ORM, RESTful APIs, and WebSocket communication.

---

## 🛠️ Tech Stack

### Frontend
- **HTML5 / CSS3 / JavaScript** — Responsive dark-themed UI with modern design.
- **Leaflet.js** — Interactive maps for real-time vehicle tracking.
- **Chart.js** — Data visualization for analytics dashboards.
- **Socket.IO (Client)** — Real-time bidirectional communication.
- **Web Speech API** — Voice command integration.

### Backend
- **Flask** — Lightweight Python web framework for REST APIs and server-side logic.
- **Flask-SocketIO** — Real-time WebSocket event handling.
- **Flask-Login** — Session-based authentication with role-based access control.
- **SQLAlchemy ORM** — Database abstraction layer.

### Machine Learning
- **XGBoost** — Gradient boosted trees for trip duration prediction.
- **Random Forest** — Ensemble model for fare and time estimation.
- **K-Means Clustering** — Spatial clustering of pickup/drop-off locations.
- **scikit-learn** — Model training, evaluation, and preprocessing.

### Database
- **SQLite** — Lightweight relational database for users, vehicles, rides, and system settings.

### Dataset
- **Porto Taxi Trajectory Dataset** (Kaggle) — 100,000+ GPS polyline records from Porto, Portugal taxis.

---

## 🖥️ Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/9346mukesh/Vehicle-Tracking-System-Using-GPS-Tracking
   cd Vehicle-Tracking-System-Using-GPS-Tracking
   ```

2. **Install dependencies:**
   ```bash
   pip install flask flask-socketio flask-cors flask-login flask-sqlalchemy
   pip install xgboost scikit-learn pandas numpy
   pip install werkzeug
   ```

3. **Initialize the database:**
   ```bash
   python complete_fix.py
   ```

4. **Start the application:**
   ```bash
   python app_complete.py
   ```

5. **Open in browser:**
   ```
   http://localhost:5000
   ```

---

## 🎯 Login Credentials (Default)

| Role     | Username   | Password     | Dashboard URL                          |
|----------|------------|--------------|----------------------------------------|
| Admin    | `admin`    | `admin123`   | http://localhost:5000/admin_dashboard   |
| Driver   | `driver1`  | `password123`| http://localhost:5000/driver_dashboard  |
| Customer | `customer1`| `password123`| http://localhost:5000/customer_dashboard|

---

## 📂 Project Structure

```
Vehicle-Tracking-System-Using-GPS-Tracking/
├── app_complete.py              # Main Flask application (entry point)
├── models.py                    # SQLAlchemy database models (User, Vehicle, Ride, SystemSettings)
├── city_config.py               # City configs for Bangalore & Porto (locations, routes, fare rules)
├── complete_fix.py              # Database initialization and fix script
├── setup_database.py            # Alternative database setup
├── seed_drivers.py              # Seed driver data into database
├── evaluate_models.py           # ML model evaluation utilities
├── cluster_metrics.py           # K-Means clustering metrics
├── pipeline_metrics.py          # ML pipeline performance metrics
├── create_scaler.py             # Feature scaler creation
├── inspect_models.py            # Inspect trained model details
├── Models/                      # Trained ML models
│   ├── Models.ipynb             # Jupyter notebook (training pipeline)
│   ├── xgboost_model.pkl        # Trained XGBoost regressor
│   ├── random_forest_model (1).pkl  # Trained Random Forest regressor
│   ├── kmeans_start.pkl         # K-Means model for start location clusters
│   ├── kmeans_end.pkl           # K-Means model for end location clusters
│   └── feature_columns.pkl     # Feature column names used during training
├── templates/                   # Jinja2 HTML templates
│   ├── landing.html             # Landing page
│   ├── login.html               # Login page
│   ├── register.html            # Registration page
│   ├── customer_dashboard.html  # Customer booking & tracking dashboard
│   ├── driver_dashboard.html    # Driver ride management dashboard
│   ├── admin_dashboard.html     # Admin fleet monitoring dashboard
│   ├── analytics.html           # Analytics & chart dashboard
│   ├── tracking.html            # Real-time GPS tracking page
│   └── index.html               # Index page
├── static/
│   ├── css/
│   │   └── style.css            # Global dark-theme styles
│   └── js/
│       ├── main.js              # Core application logic
│       ├── tracking.js          # Real-time GPS tracking with Leaflet.js
│       ├── analytics.js         # Chart.js analytics visualizations
│       └── voice-assistant.js   # Web Speech API voice commands
├── instance/
│   └── rideshare.db             # SQLite database 
├── SYSTEM_ARCHITECTURE.md       # Detailed system architecture documentation
├── ARCHITECTURE_DIAGRAMS.md     # Architecture diagrams
└── README.md                    # Project documentation (this file)
```

---

## 📊 Features Breakdown

### Customer Dashboard
- **Ride Booking** — Select pickup and drop-off from pre-configured city locations.
- **Fare Estimation** — Get instant fare estimates powered by ML models before booking.
- **Real-Time Tracking** — Watch driver approach on a live map after booking.
- **Ride History** — View past rides with fare, distance, and status details.
- **Voice Commands** — Book rides, check status, and navigate hands-free.

### Driver Dashboard
- **Ride Requests** — View and accept pending ride requests in real time.
- **Navigation** — GPS-guided pickup and drop-off navigation.
- **Earnings Tracker** — Monitor daily trips, earnings, and online hours.
- **Status Toggle** — Go online/offline to control ride availability.

### Admin Dashboard
- **Fleet Map** — Monitor all vehicles on a live map with real-time position updates.
- **System Statistics** — Total rides, active rides, revenue, and driver availability.
- **Vehicle Management** — Track individual vehicles by registration number.
- **Analytics** — Trip distance distribution, duration analysis, speed metrics, and hourly demand charts.

### Machine Learning Pipeline

| Model | Purpose | Algorithm |
|-------|---------|-----------|
| ETA Predictor | Trip duration estimation | XGBoost Regressor |
| Fare Predictor | Fare and time estimation | Random Forest Regressor |
| Start Clustering | Pickup location grouping | K-Means (150 clusters) |
| End Clustering | Drop-off location grouping | K-Means (180 clusters) |

**Features Used:** `start_lat`, `start_lon`, `end_lat`, `end_lon`, `distance`, `bearing`, `straightness`, `num_points`, `hour`, `day_of_week`, `month`, `is_weekend`, `is_rush_hour`, `start_cluster`, `end_cluster`

---

## 🧪 Testing

### Backend
- Test all REST API endpoints using **Postman** or **cURL**.
- Verify role-based access control for customer, driver, and admin routes.
- Validate ML model predictions against known trip durations.

### Frontend
- Verify real-time map updates via WebSocket connections.
- Test voice assistant commands across all three dashboards.
- Ensure responsive design on desktop and mobile viewports.

### End-to-End
- Complete ride lifecycle: Book → Accept → Track → Complete → Rate.
- Validate fare calculation with dynamic pricing across different times of day.
- Stress test with simulated concurrent vehicle movements.

---

## 🏗️ Future Enhancements

- **Push Notifications** — Real-time alerts via Firebase Cloud Messaging for ride updates.
- **Payment Gateway Integration** — Razorpay/Stripe for in-app payments.
- **Advanced ML Models** — LSTM/Transformer-based ETA prediction for improved accuracy.
- **Multi-Language Support** — Localization for regional languages.
- **Driver Heatmaps** — Visualize demand hotspots to help drivers optimize positioning.
- **Ride Sharing / Carpooling** — Match multiple passengers with similar routes.
- **Data Export** — CSV/PDF export of ride history and analytics reports.

---

## 📸 Screenshots

> Refer the ScreenShot Folder

<!--  Refer the ScreenShot Folder
Screenshots of your application pages:
![Landing Page](screenshots/landing.png)
![Customer Dashboard](screenshots/customer_dashboard.png)
![Driver Dashboard](screenshots/driver_dashboard.png)
![Admin Dashboard](screenshots/admin_dashboard.png)
![Analytics](screenshots/analytics.png)
![Real-Time Tracking](screenshots/tracking.png)
-->

---


## 👥 Contributors
Mukesh Kumar Reddy - Team Lead & Software Developer

Kanush - Web Developer

Lokesh - Tester

Tejeswar - Content Writer & Data Preparation for ML training
## 📬 Contact

For questions or contributions, reach out:

- **GitHub:** [https://github.com/9346mukesh](https://github.com/9346mukesh)

---

> **Built with Flask, XGBoost, and Real-Time GPS Simulation** 🚀
