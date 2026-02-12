"""
GPS-Based Vehicle Tracking System with ML-Enhanced Route Prediction
Complete Backend with Role-Based Dashboards, Voice Integration, and Real-time GPS Streaming
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import pickle
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
import threading
import random
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Vehicle, Ride, SystemSettings
from city_config import (
    BANGALORE_CONFIG, PORTO_CONFIG, BANGALORE_VEHICLES, PORTO_VEHICLES,
    get_city_config, get_vehicles_for_city, calculate_fare, get_all_locations
)

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gps_tracking_secret_key_2026'

# Get the absolute path to the database directory
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'rideshare.db')

# Ensure instance directory exists
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

# Initialize extensions
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load trained ML models
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
simulated_vehicles = {}
vehicle_movement_thread_started = False
pending_rides = []

# ========================
# Helper Functions
# ========================

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates in kilometers"""
    R = 6371
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
    return (np.degrees(initial_bearing) + 360) % 360

def predict_trip_duration(start_lat, start_lon, end_lat, end_lon, hour, day_of_week, month):
    """Predict trip duration using ML model"""
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

def init_simulated_vehicles():
    """Initialize 10 simulated vehicles for Bangalore"""
    global simulated_vehicles
    
    # Only initialize if not already done
    if simulated_vehicles:
        return
    
    locations = list(BANGALORE_CONFIG['locations'].values())
    
    for i, vehicle_data in enumerate(BANGALORE_VEHICLES):
        # Assign random location
        location = random.choice(locations)
        
        simulated_vehicles[vehicle_data['id']] = {
            'id': vehicle_data['id'],
            'number': vehicle_data['id'],
            'type': vehicle_data['type'],
            'model': vehicle_data['model'],
            'color': vehicle_data['color'],
            'city': 'bangalore',
            'lat': location['lat'] + random.uniform(-0.01, 0.01),
            'lon': location['lon'] + random.uniform(-0.01, 0.01),
            'status': 'available',
            'driver_name': f'Driver {i+1}',
            'rating': round(random.uniform(4.0, 5.0), 1),
            'total_trips': random.randint(50, 500)
        }
    
    # Start simulation thread
    thread = threading.Thread(target=simulate_vehicle_movement)
    thread.daemon = True
    thread.start()

def simulate_vehicle_movement():
    """Simulate random movement for idle vehicles"""
    while True:
        for vehicle_id, vehicle in simulated_vehicles.items():
            if vehicle['status'] == 'available':
                # Small random movement
                vehicle['lat'] += random.uniform(-0.001, 0.001)
                vehicle['lon'] += random.uniform(-0.001, 0.001)
                
                # Emit update
                socketio.emit('vehicle_update', {
                    'vehicle_id': vehicle_id,
                    'lat': vehicle['lat'],
                    'lon': vehicle['lon'],
                    'status': vehicle['status']
                })
        
        time.sleep(5)  # Update every 5 seconds

def simulate_vehicle_movement_db():
    """Simulate movement for vehicles stored in the database"""
    while True:
        with app.app_context():
            vehicles = Vehicle.query.filter(
                Vehicle.current_lat.isnot(None),
                Vehicle.current_lon.isnot(None)
            ).all()

            for vehicle in vehicles:
                if vehicle.status == 'offline':
                    continue

                vehicle.current_lat += random.uniform(-0.0008, 0.0008)
                vehicle.current_lon += random.uniform(-0.0008, 0.0008)

                socketio.emit('vehicle_update', {
                    'vehicle_id': vehicle.vehicle_number,
                    'lat': vehicle.current_lat,
                    'lon': vehicle.current_lon,
                    'status': vehicle.status
                })

            db.session.commit()

        time.sleep(5)  # Update every 5 seconds

def start_vehicle_movement_thread():
    """Start a single background thread for vehicle movement"""
    global vehicle_movement_thread_started
    if vehicle_movement_thread_started:
        return
    vehicle_movement_thread_started = True
    thread = threading.Thread(target=simulate_vehicle_movement_db)
    thread.daemon = True
    thread.start()

# ========================
# Authentication Routes
# ========================

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Support both JSON and form data
        if request.is_json:
            data = request.json
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            # Return JSON if request was JSON, otherwise redirect
            if request.is_json:
                return jsonify({
                    'success': True,
                    'role': user.role,
                    'redirect': f'/{user.role}_dashboard'
                })
            else:
                # Redirect based on role
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user.role == 'driver':
                    return redirect(url_for('driver_dashboard'))
                else:
                    return redirect(url_for('customer_dashboard'))
        
        # Handle failed login
        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Support both JSON and form data
        if request.is_json:
            data = request.json
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            full_name = data.get('full_name')
            phone = data.get('phone')
            role = data.get('role', 'customer')
            vehicle_number = data.get('vehicle_number')
            vehicle_type = data.get('vehicle_type', 'sedan')
            vehicle_model = data.get('vehicle_model', 'Honda City')
            vehicle_color = data.get('vehicle_color', 'White')
        else:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            role = request.form.get('role', 'customer')
            vehicle_number = request.form.get('vehicle_number')
            vehicle_type = request.form.get('vehicle_type', 'sedan')
            vehicle_model = request.form.get('vehicle_model', 'Honda City')
            vehicle_color = request.form.get('vehicle_color', 'White')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username already exists'})
            else:
                flash('Username already exists', 'error')
                return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Email already exists'})
            else:
                flash('Email already exists', 'error')
                return redirect(url_for('register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # If driver, create vehicle
        if user.role == 'driver':
            vehicle = Vehicle(
                driver_id=user.id,
                vehicle_number=vehicle_number or f'KA-01-{random.randint(1000,9999)}',
                vehicle_type=vehicle_type,
                vehicle_model=vehicle_model,
                vehicle_color=vehicle_color,
                city='bangalore'
            )
            db.session.add(vehicle)
            db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Registration successful'})
        else:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

# ========================
# Dashboard Routes
# ========================

@app.route('/customer_dashboard')
@login_required
def customer_dashboard():
    if current_user.role != 'customer':
        return redirect(url_for('landing'))
    return render_template('customer_dashboard.html', user=current_user)

@app.route('/driver_dashboard')
@login_required
def driver_dashboard():
    if current_user.role != 'driver':
        return redirect(url_for('landing'))
    return render_template('driver_dashboard.html', user=current_user)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('landing'))
    return render_template('admin_dashboard.html', user=current_user)

@app.route('/analytics')
@login_required
def analytics_dashboard():
    return render_template('analytics.html')

def build_bins(values, edges, labels):
    counts = [0] * (len(edges) - 1)
    for value in values:
        for i in range(len(edges) - 1):
            if edges[i] <= value < edges[i + 1]:
                counts[i] += 1
                break
    return {'labels': labels, 'values': counts}

# ========================
# API Endpoints
# ========================

@app.route('/api/locations/<city>')
def get_locations(city):
    """Get all locations for a city"""
    config = get_city_config(city)
    return jsonify({'locations': config['locations']})

@app.route('/api/nearby-vehicles/<city>')
def get_nearby_vehicles(city):
    """Get nearby available vehicles"""
    vehicles = Vehicle.query.filter_by(city=city, status='available').all()
    return jsonify({
        'count': len(vehicles),
        'vehicles': [v.to_dict() for v in vehicles]
    })

@app.route('/api/estimate-fare', methods=['POST'])
def estimate_fare():
    """Estimate fare for a ride"""
    data = request.json
    city = data['city']
    config = get_city_config(city)
    
    pickup_loc = config['locations'][data['pickup_location']]
    dropoff_loc = config['locations'][data['dropoff_location']]
    
    distance = haversine_distance(
        pickup_loc['lat'], pickup_loc['lon'],
        dropoff_loc['lat'], dropoff_loc['lon']
    )
    
    now = datetime.now()
    fare = calculate_fare(distance, city, now.hour)
    
    return jsonify({
        'fare': fare,
        'distance': distance,
        'currency': config['currency']
    })

@app.route('/api/driver/summary')
@login_required
def driver_summary():
    if current_user.role != 'driver':
        return jsonify({'error': 'Unauthorized'}), 403

    today = datetime.now().date()
    rides_query = Ride.query.filter(
        Ride.driver_id == current_user.id,
        db.func.date(Ride.created_at) == today
    )

    trips_today = rides_query.filter(Ride.status != 'cancelled').count()
    earnings_today = rides_query.filter(Ride.status == 'completed') \
        .with_entities(db.func.sum(Ride.fare)).scalar() or 0
    minutes_today = rides_query.filter(Ride.status.in_(['completed', 'in_progress'])) \
        .with_entities(db.func.sum(Ride.duration)).scalar() or 0

    return jsonify({
        'trips_today': trips_today,
        'earnings_today': float(earnings_today),
        'online_hours': float(minutes_today) / 60 if minutes_today else 0
    })

@app.route('/api/customer/recent-rides')
@login_required
def customer_recent_rides():
    if current_user.role != 'customer':
        return jsonify({'error': 'Unauthorized'}), 403

    rides = Ride.query.filter_by(customer_id=current_user.id) \
        .order_by(Ride.created_at.desc()).limit(10).all()

    return jsonify({
        'rides': [
            {
                'date': r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else '-',
                'pickup_address': r.pickup_address or '-',
                'dropoff_address': r.dropoff_address or '-',
                'fare': float(r.fare or 0),
                'status': r.status or 'unknown'
            }
            for r in rides
        ]
    })

@app.route('/api/analytics')
@login_required
def get_analytics():
    rides = Ride.query.order_by(Ride.created_at.desc()).all()

    distances = [r.distance or 0 for r in rides]
    durations = [r.duration or 0 for r in rides]
    speeds = [
        (r.distance / (r.duration / 60)) if r.distance and r.duration else 0
        for r in rides
    ]

    total_trips = len(rides)
    total_distance = sum(distances)
    total_duration_minutes = sum(durations)
    total_duration_hours = total_duration_minutes / 60 if total_duration_minutes else 0
    avg_speed = (total_distance / total_duration_hours) if total_duration_hours else 0

    distance_bins = build_bins(
        distances,
        [0, 5, 10, 15, 20, float('inf')],
        ['0-5 km', '5-10 km', '10-15 km', '15-20 km', '20+ km']
    )
    duration_bins = build_bins(
        durations,
        [0, 10, 20, 30, 40, float('inf')],
        ['0-10 min', '10-20 min', '20-30 min', '30-40 min', '40+ min']
    )
    speed_bins = build_bins(
        speeds,
        [0, 20, 40, 60, 80, float('inf')],
        ['0-20', '20-40', '40-60', '60-80', '80+']
    )

    hourly_labels = ['00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00']
    hourly_values = [0] * len(hourly_labels)
    for ride in rides:
        if not ride.created_at:
            continue
        bucket = (ride.created_at.hour // 3)
        if 0 <= bucket < len(hourly_values):
            hourly_values[bucket] += 1

    driver_ids = {r.driver_id for r in rides if r.driver_id}
    vehicles = Vehicle.query.filter(Vehicle.driver_id.in_(driver_ids)).all() if driver_ids else []
    vehicle_by_driver = {v.driver_id: v for v in vehicles}

    trip_rows = []
    for ride in rides[:50]:
        vehicle = vehicle_by_driver.get(ride.driver_id)
        distance = ride.distance or 0
        duration = ride.duration or 0
        speed = (distance / (duration / 60)) if duration else 0
        trip_rows.append({
            'vehicle_id': vehicle.vehicle_number if vehicle else None,
            'date': ride.created_at.strftime('%Y-%m-%d %H:%M') if ride.created_at else '- ',
            'distance': float(distance),
            'duration': float(duration),
            'speed': float(speed),
            'status': ride.status
        })

    return jsonify({
        'summary': {
            'total_trips': total_trips,
            'total_distance_km': float(total_distance),
            'total_time_hours': float(total_duration_hours),
            'avg_speed_kmh': float(avg_speed)
        },
        'charts': {
            'distance_bins': distance_bins,
            'duration_bins': duration_bins,
            'speed_bins': speed_bins,
            'hourly': {
                'labels': hourly_labels,
                'values': hourly_values
            }
        },
        'trips': trip_rows
    })

@app.route('/api/book-ride', methods=['POST'])
@login_required
def book_ride():
    """Book a new ride"""
    data = request.json
    city = data['city']
    config = get_city_config(city)
    
    pickup_loc = config['locations'][data['pickup_location']]
    dropoff_loc = config['locations'][data['dropoff_location']]
    
    distance = haversine_distance(
        pickup_loc['lat'], pickup_loc['lon'],
        dropoff_loc['lat'], dropoff_loc['lon']
    )
    
    now = datetime.now()
    fare = calculate_fare(distance, city, now.hour)
    duration_sec, duration_min = predict_trip_duration(
        pickup_loc['lat'], pickup_loc['lon'],
        dropoff_loc['lat'], dropoff_loc['lon'],
        now.hour, now.weekday(), now.month
    )
    
    ride = Ride(
        customer_id=current_user.id,
        pickup_lat=pickup_loc['lat'],
        pickup_lon=pickup_loc['lon'],
        pickup_address=pickup_loc['name'],
        dropoff_lat=dropoff_loc['lat'],
        dropoff_lon=dropoff_loc['lon'],
        dropoff_address=dropoff_loc['name'],
        city=city,
        distance=distance,
        duration=duration_min,
        fare=fare,
        status='pending'
    )
    
    db.session.add(ride)
    db.session.commit()
    
    # Add to pending rides
    pending_rides.append(ride.id)
    
    # Notify drivers
    socketio.emit('new_ride', ride.to_dict())
    
    return jsonify({'success': True, 'ride': ride.to_dict()})

@app.route('/api/driver/pending-rides')
@login_required
def get_pending_rides():
    """Get pending ride requests for driver"""
    if current_user.role != 'driver':
        return jsonify({'error': 'Unauthorized'}), 403
    
    rides = Ride.query.filter_by(status='pending').all()
    return jsonify({'rides': [r.to_dict() for r in rides]})

@app.route('/api/driver/accept-ride/<int:ride_id>', methods=['POST'])
@login_required
def accept_ride(ride_id):
    """Accept a ride request"""
    if current_user.role != 'driver':
        return jsonify({'error': 'Unauthorized'}), 403
    
    ride = Ride.query.get(ride_id)
    if not ride or ride.status != 'pending':
        return jsonify({'success': False, 'message': 'Ride not available'})
    
    ride.driver_id = current_user.id
    ride.status = 'accepted'
    ride.accepted_at = datetime.utcnow()
    
    db.session.commit()
    
    # Remove from pending
    if ride_id in pending_rides:
        pending_rides.remove(ride_id)
    
    # Notify customer
    socketio.emit('ride_update', {'ride_id': ride_id, 'status': 'accepted'})
    
    return jsonify({'success': True, 'ride': ride.to_dict()})

@app.route('/api/driver/status', methods=['POST'])
@login_required
def update_driver_status():
    """Update driver online/offline status"""
    if current_user.role != 'driver':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    vehicle = Vehicle.query.filter_by(driver_id=current_user.id).first()
    
    if vehicle:
        vehicle.status = 'available' if data['online'] else 'offline'
        db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/admin/stats')
@login_required
def get_admin_stats():
    """Get statistics for admin dashboard"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    city = request.args.get('city', 'all')
    
    # Get today's rides
    today = datetime.now().date()
    query = Ride.query.filter(db.func.date(Ride.created_at) == today)
    
    if city != 'all':
        query = query.filter_by(city=city)
    
    total_rides = query.count()
    active_rides = query.filter_by(status='in_progress').count()
    total_revenue = query.with_entities(db.func.sum(Ride.fare)).scalar() or 0
    
    # Get driver stats
    vehicle_query = Vehicle.query
    if city != 'all':
        vehicle_query = vehicle_query.filter_by(city=city)
    
    total_drivers = vehicle_query.count()
    available_drivers = vehicle_query.filter_by(status='available').count()
    
    return jsonify({
        'total_rides': total_rides,
        'active_rides': active_rides,
        'total_revenue': round(total_revenue, 2),
        'total_drivers': total_drivers,
        'available_drivers': available_drivers
    })

@app.route('/api/admin/vehicles')
@login_required
def get_all_vehicles():
    """Get all vehicles for admin"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    city = request.args.get('city', 'all')
    vehicles_query = Vehicle.query
    if city != 'all':
        vehicles_query = vehicles_query.filter_by(city=city)

    vehicles = []
    for vehicle in vehicles_query.all():
        vehicle_data = vehicle.to_dict()
        vehicle_data['driver_name'] = vehicle.owner.full_name if vehicle.owner else None
        vehicles.append(vehicle_data)
    
    return jsonify({'vehicles': vehicles})

@app.route('/api/admin/track/<vehicle_number>')
@login_required
def track_vehicle(vehicle_number):
    """Track a specific vehicle"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()
    if not vehicle:
        return jsonify({'success': False, 'message': 'Vehicle not found'})

    if vehicle.current_lat is None or vehicle.current_lon is None:
        return jsonify({'success': False, 'message': 'Vehicle location not available'})

    return jsonify({
        'success': True,
        'vehicle': vehicle.to_dict(),
        'location': {'lat': vehicle.current_lat, 'lon': vehicle.current_lon}
    })

# ========================
# WebSocket Events
# ========================

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'message': 'Connected to RideShare Pro server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# ========================
# Initialize Database
# ========================

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@rideshare.com',
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created: username=admin, password=admin123")

# ========================
# Main Entry Point
# ========================

if __name__ == '__main__':
    init_database()
    start_vehicle_movement_thread()
    
    print("\n" + "="*80)
    print("RIDESHARE PRO - GPS VEHICLE TRACKING SYSTEM")
    print("="*80)
    print("\nServer Features:")
    print("  ✓ Role-Based Access Control (Customer, Driver, Admin)")
    print("  ✓ Voice Integration Support")
    print("  ✓ GPS Simulation (10 Bangalore Vehicles)")
    print("  ✓ Real-time Vehicle Tracking")
    print("  ✓ ML-Powered Route Prediction")
    print("\nAccess Points:")
    print("  Landing Page: http://localhost:5000")
    print("  Login: http://localhost:5000/login")
    print("  Register: http://localhost:5000/register")
    print("\nDefault Admin Login:")
    print("  Username: admin")
    print("  Password: admin123")
    print("="*80 + "\n")
    
    port = int(os.environ.get('FLASK_PORT', 5000))
    socketio.run(app, debug=False, use_reloader=False, host='127.0.0.1', port=port)
