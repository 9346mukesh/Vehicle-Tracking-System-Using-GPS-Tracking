"""
GPS-Based Vehicle Tracking System with ML-Enhanced Route Prediction
Backend Flask Application with Real-time GPS Streaming
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime
import threading
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gps_tracking_secret_key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load trained models
print("Loading ML models...")
with open('Models/xgboost_model.pkl', 'rb') as f:
    xgb_model = pickle.load(f)

with open('Models/random_forest_model (1).pkl', 'rb') as f:
    rf_model = pickle.load(f)

with open('Models/kmeans_start.pkl', 'rb') as f:
    kmeans_start = pickle.load(f)

with open('Models/kmeans_end.pkl', 'rb') as f:
    kmeans_end = pickle.load(f)

with open('Models/feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

print("✓ All models loaded successfully!")

# Global variables
active_vehicles = {}
simulation_active = False

# Helper Functions
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates"""
    R = 6371  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate bearing between two points"""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    initial_bearing = np.arctan2(x, y)
    initial_bearing = np.degrees(initial_bearing)
    return (initial_bearing + 360) % 360

def interpolate_route(start_lat, start_lon, end_lat, end_lon, num_points=50):
    """Generate smooth GPS points between start and end"""
    lats = np.linspace(start_lat, end_lat, num_points)
    lons = np.linspace(start_lon, end_lon, num_points)
    
    # Add some randomness for realistic routes
    noise_lat = np.random.normal(0, 0.001, num_points)
    noise_lon = np.random.normal(0, 0.001, num_points)
    
    lats += noise_lat
    lons += noise_lon
    
    return list(zip(lats, lons))

def predict_trip_duration(start_lat, start_lon, end_lat, end_lon, hour, day_of_week, month):
    """Predict trip duration using trained model"""
    distance = haversine_distance(start_lat, start_lon, end_lat, end_lon)
    bearing = calculate_bearing(start_lat, start_lon, end_lat, end_lon)
    num_points = max(2, int(distance * 10))
    straightness = 0.8
    is_weekend = 1 if day_of_week in [5, 6] else 0
    is_rush_hour = 1 if hour in [7, 8, 9, 17, 18, 19] else 0
    
    start_cluster = kmeans_start.predict([[start_lat, start_lon]])[0]
    end_cluster = kmeans_end.predict([[end_lat, end_lon]])[0]
    
    features = pd.DataFrame([[
        start_lat, start_lon, end_lat, end_lon,
        distance, bearing, straightness, num_points,
        hour, day_of_week, month, is_weekend, is_rush_hour,
        start_cluster, end_cluster
    ]], columns=feature_columns)
    
    duration_seconds = xgb_model.predict(features)[0]
    return duration_seconds, duration_seconds / 60

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tracking')
def tracking():
    return render_template('tracking.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for trip prediction"""
    data = request.json
    
    start_lat = float(data['start_lat'])
    start_lon = float(data['start_lon'])
    end_lat = float(data['end_lat'])
    end_lon = float(data['end_lon'])
    
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    month = now.month
    
    duration_sec, duration_min = predict_trip_duration(
        start_lat, start_lon, end_lat, end_lon, hour, day_of_week, month
    )
    
    distance = haversine_distance(start_lat, start_lon, end_lat, end_lon)
    avg_speed = (distance / duration_sec) * 3600 if duration_sec > 0 else 0
    
    return jsonify({
        'success': True,
        'duration_seconds': float(duration_sec),
        'duration_minutes': float(duration_min),
        'distance_km': float(distance),
        'avg_speed_kmh': float(avg_speed),
        'eta': (now.timestamp() + duration_sec) * 1000
    })

@app.route('/api/start_simulation', methods=['POST'])
def start_simulation():
    """Start GPS simulation for a vehicle"""
    data = request.json
    vehicle_id = data['vehicle_id']
    start_lat = float(data['start_lat'])
    start_lon = float(data['start_lon'])
    end_lat = float(data['end_lat'])
    end_lon = float(data['end_lon'])
    
    # Generate route
    route = interpolate_route(start_lat, start_lon, end_lat, end_lon, num_points=100)
    
    # Predict duration
    now = datetime.now()
    duration_sec, duration_min = predict_trip_duration(
        start_lat, start_lon, end_lat, end_lon, 
        now.hour, now.weekday(), now.month
    )
    
    active_vehicles[vehicle_id] = {
        'route': route,
        'current_index': 0,
        'start_time': time.time(),
        'duration': duration_sec,
        'distance': haversine_distance(start_lat, start_lon, end_lat, end_lon),
        'status': 'active'
    }
    
    # Start background thread for GPS streaming
    thread = threading.Thread(target=simulate_gps_stream, args=(vehicle_id,))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'vehicle_id': vehicle_id,
        'total_points': len(route),
        'estimated_duration': duration_min
    })

def simulate_gps_stream(vehicle_id):
    """Simulate real-time GPS data streaming"""
    while vehicle_id in active_vehicles:
        vehicle = active_vehicles[vehicle_id]
        
        if vehicle['current_index'] >= len(vehicle['route']):
            vehicle['status'] = 'completed'
            socketio.emit('vehicle_completed', {'vehicle_id': vehicle_id})
            break
        
        current_point = vehicle['route'][vehicle['current_index']]
        elapsed_time = time.time() - vehicle['start_time']
        progress = (vehicle['current_index'] / len(vehicle['route'])) * 100
        
        # Calculate current speed
        if vehicle['current_index'] > 0:
            prev_point = vehicle['route'][vehicle['current_index'] - 1]
            segment_distance = haversine_distance(
                prev_point[0], prev_point[1],
                current_point[0], current_point[1]
            )
            speed = segment_distance * 3600  # km/h (assuming 1 second per point)
        else:
            speed = 0
        
        gps_data = {
            'vehicle_id': vehicle_id,
            'latitude': current_point[0],
            'longitude': current_point[1],
            'speed': speed,
            'timestamp': datetime.now().isoformat(),
            'progress': progress,
            'elapsed_time': elapsed_time,
            'distance_covered': (vehicle['distance'] * progress / 100)
        }
        
        socketio.emit('gps_update', gps_data)
        
        vehicle['current_index'] += 1
        time.sleep(0.5)  # Update every 0.5 seconds

@app.route('/api/stop_simulation/<vehicle_id>', methods=['POST'])
def stop_simulation(vehicle_id):
    """Stop GPS simulation"""
    if vehicle_id in active_vehicles:
        del active_vehicles[vehicle_id]
        return jsonify({'success': True, 'message': 'Simulation stopped'})
    return jsonify({'success': False, 'message': 'Vehicle not found'})

@app.route('/api/vehicles')
def get_vehicles():
    """Get all active vehicles"""
    return jsonify({
        'vehicles': [
            {
                'id': vid,
                'status': data['status'],
                'progress': (data['current_index'] / len(data['route'])) * 100
            }
            for vid, data in active_vehicles.items()
        ]
    })

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'data': 'Connected to GPS tracking server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    print("\n" + "="*80)
    print("GPS-BASED VEHICLE TRACKING SYSTEM")
    print("="*80)
    print("\nServer starting...")
    print("Dashboard: http://localhost:5000")
    print("="*80 + "\n")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
