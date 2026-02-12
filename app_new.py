"""
GPS-Based Vehicle Tracking System with Role-Based Access Control
Enhanced Flask Application with Authentication and Multiple Cities
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
import pickle
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime
import threading
import random
import os

# Import models and configurations
from models import db, User, Vehicle, Ride
from city_config import (
    get_city_config, get_vehicles_for_city, calculate_fare,
    get_location_by_name, get_all_locations
)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tracking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Load ML models
print("Loading ML models...")
try:
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
    
    print("✓ All ML models loaded successfully!")
except Exception as e:
    print(f"⚠ Warning: Could not load ML models: {e}")
    xgb_model = None

# Global variables
active_vehicles = {}
active_rides = {}
vehicle_movement_thread_started = False

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Role-based access decorator
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Helper Functions
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates"""
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
    initial_bearing = np.degrees(initial_bearing)
    return (initial_bearing + 360) % 360

def interpolate_route(start_lat, start_lon, end_lat, end_lon, num_points=50):
    """Generate smooth GPS points between start and end"""
    lats = np.linspace(start_lat, end_lat, num_points)
    lons = np.linspace(start_lon, end_lon, num_points)
    noise_lat = np.random.normal(0, 0.001, num_points)
    noise_lon = np.random.normal(0, 0.001, num_points)
    lats += noise_lat
    lons += noise_lon
    return list(zip(lats, lons))

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

def predict_trip_duration(start_lat, start_lon, end_lat, end_lon, hour, day_of_week, month):
    """Predict trip duration using trained model"""
    if xgb_model is None:
        distance = haversine_distance(start_lat, start_lon, end_lat, end_lon)
        avg_speed = 30
        duration_seconds = (distance / avg_speed) * 3600
        return duration_seconds, duration_seconds / 60
    
    distance = haversine_distance(start_lat, start_lon, end_lat, end_lon)
    bearing = calculate_bearing(start_lat, start_lon, end_lat, end_lon)
    num_points = max(2, int(distance * 10))
    straightness = 0.8
    is_weekend = 1 if day_of_week in [5, 6] else 0
    is_rush_hour = 1 if hour in [7, 8, 9, 17, 18, 19] else 0
    
    try:
        start_cluster = kmeans_start.predict([[start_lat, start_lon]])[0]
        end_cluster = kmeans_end.predict([[end_lat, end_lon]])[0]
    except:
        start_cluster = 0
        end_cluster = 0
    
    features = pd.DataFrame([[
        start_lat, start_lon, end_lat, end_lon,
        distance, bearing, straightness, num_points,
        hour, day_of_week, month, is_weekend, is_rush_hour,
        start_cluster, end_cluster
    ]], columns=feature_columns)
    
    duration_seconds = xgb_model.predict(features)[0]
    return duration_seconds, duration_seconds / 60

# Authentication Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'driver':
                return redirect(url_for('driver_dashboard'))
            else:
                return redirect(url_for('customer_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        role = request.form.get('role', 'customer')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, role=role, full_name=full_name, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Redirect to appropriate dashboard"""
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'driver':
        return redirect(url_for('driver_dashboard'))
    else:
        return redirect(url_for('customer_dashboard'))

@app.route('/dashboard/customer')
@role_required('customer')
def customer_dashboard():
    """Customer dashboard"""
    rides = Ride.query.filter_by(customer_id=current_user.id).order_by(Ride.created_at.desc()).limit(10).all()
    return render_template('customer_dashboard.html', rides=rides)

@app.route('/dashboard/driver')
@role_required('driver')
def driver_dashboard():
    """Driver dashboard"""
    vehicle = Vehicle.query.filter_by(driver_id=current_user.id).first()
    rides = Ride.query.filter_by(driver_id=current_user.id).order_by(Ride.created_at.desc()).limit(10).all()
    pending_rides = Ride.query.filter_by(status='pending').order_by(Ride.created_at.desc()).limit(5).all()
    return render_template('driver_dashboard.html', user=current_user, vehicle=vehicle, rides=rides, pending_rides=pending_rides)

@app.route('/dashboard/admin')
@role_required('admin')
def admin_dashboard():
    """Admin dashboard"""
    vehicles = Vehicle.query.all()
    total_rides = Ride.query.count()
    active_rides = Ride.query.filter(Ride.status.in_(['accepted', 'in_progress'])).count()
    total_drivers = User.query.filter_by(role='driver').count()
    total_customers = User.query.filter_by(role='customer').count()
    stats = {
        'total_rides': total_rides,
        'active_rides': active_rides,
        'total_drivers': total_drivers,
        'total_customers': total_customers,
        'available_drivers': Vehicle.query.filter_by(status='available').count()
    }
    return render_template('admin_dashboard.html', vehicles=vehicles, stats=stats)

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

# API Routes
@app.route('/api/admin/stats')
@login_required
def get_admin_stats():
    """Get statistics for admin dashboard"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    city = request.args.get('city', 'all')

    today = datetime.now().date()
    query = Ride.query.filter(db.func.date(Ride.created_at) == today)
    if city != 'all':
        query = query.filter_by(city=city)

    total_rides = query.count()
    active_rides = query.filter_by(status='in_progress').count()
    total_revenue = query.with_entities(db.func.sum(Ride.fare)).scalar() or 0

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

@app.route('/api/cities')
def get_cities():
    return jsonify({'cities': [{'id': 'bangalore', 'name': 'Bangalore', 'country': 'India'}, {'id': 'porto', 'name': 'Porto', 'country': 'Portugal'}]})

@app.route('/api/city/<city_name>')
def get_city_info(city_name):
    config = get_city_config(city_name)
    return jsonify(config)

@app.route('/api/locations/<city_name>')
def get_city_locations(city_name):
    locations = get_all_locations(city_name)
    return jsonify({'locations': locations})

@app.route('/api/vehicles/<city_name>')
def get_available_vehicles(city_name):
    vehicles = Vehicle.query.filter_by(city=city_name, status='available').all()
    return jsonify({'vehicles': [v.to_dict() for v in vehicles]})

@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    data = request.json
    start_lat = float(data['start_lat'])
    start_lon = float(data['start_lon'])
    end_lat = float(data['end_lat'])
    end_lon = float(data['end_lon'])
    city = data.get('city', 'bangalore')
    
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    month = now.month
    
    duration_sec, duration_min = predict_trip_duration(start_lat, start_lon, end_lat, end_lon, hour, day_of_week, month)
    distance = haversine_distance(start_lat, start_lon, end_lat, end_lon)
    avg_speed = (distance / duration_sec) * 3600 if duration_sec > 0 else 0
    fare = calculate_fare(distance, city, hour)
    
    return jsonify({
        'success': True, 'duration_seconds': float(duration_sec), 'duration_minutes': float(duration_min),
        'distance_km': float(distance), 'avg_speed_kmh': float(avg_speed), 'fare': float(fare),
        'eta': (now.timestamp() + duration_sec) * 1000
    })

@app.route('/api/book_ride', methods=['POST'])
@role_required('customer')
def book_ride():
    data = request.json
    ride = Ride(
        customer_id=current_user.id, pickup_lat=float(data['pickup_lat']), pickup_lon=float(data['pickup_lon']),
        pickup_address=data.get('pickup_address', ''), dropoff_lat=float(data['dropoff_lat']), 
        dropoff_lon=float(data['dropoff_lon']), dropoff_address=data.get('dropoff_address', ''),
        city=data.get('city', 'bangalore'), distance=float(data.get('distance', 0)),
        duration=float(data.get('duration', 0)), fare=float(data.get('fare', 0)), status='pending'
    )
    db.session.add(ride)
    db.session.commit()
    socketio.emit('new_ride', ride.to_dict(), room='drivers')
    return jsonify({'success': True, 'ride_id': ride.id, 'message': 'Ride booked successfully'})

@app.route('/api/accept_ride/<int:ride_id>', methods=['POST'])
@role_required('driver')
def accept_ride(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    if ride.status != 'pending':
        return jsonify({'success': False, 'message': 'Ride already accepted'}), 400
    ride.driver_id = current_user.id
    ride.status = 'accepted'
    ride.accepted_at = datetime.utcnow()
    vehicle = Vehicle.query.filter_by(driver_id=current_user.id).first()
    if vehicle:
        vehicle.status = 'busy'
    db.session.commit()
    socketio.emit('ride_accepted', ride.to_dict(), room=f'customer_{ride.customer_id}')
    return jsonify({'success': True, 'ride': ride.to_dict()})

@app.route('/api/start_ride/<int:ride_id>', methods=['POST'])
@role_required('driver')
def start_ride(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    if ride.driver_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    ride.status = 'in_progress'
    ride.started_at = datetime.utcnow()
    db.session.commit()
    socketio.emit('ride_started', ride.to_dict(), room=f'customer_{ride.customer_id}')
    thread = threading.Thread(target=simulate_ride, args=(ride_id,))
    thread.daemon = True
    thread.start()
    return jsonify({'success': True, 'ride': ride.to_dict()})

@app.route('/api/complete_ride/<int:ride_id>', methods=['POST'])
@role_required('driver')
def complete_ride(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    if ride.driver_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    ride.status = 'completed'
    ride.completed_at = datetime.utcnow()
    vehicle = Vehicle.query.filter_by(driver_id=current_user.id).first()
    if vehicle:
        vehicle.status = 'available'
        vehicle.total_trips += 1
    db.session.commit()
    socketio.emit('ride_completed', ride.to_dict(), room=f'customer_{ride.customer_id}')
    return jsonify({'success': True, 'ride': ride.to_dict()})

@app.route('/api/cancel_ride/<int:ride_id>', methods=['POST'])
@login_required
def cancel_ride(ride_id):
    ride = Ride.query.get_or_404(ride_id)
    if ride.customer_id != current_user.id and ride.driver_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    ride.status = 'cancelled'
    if ride.driver_id:
        vehicle = Vehicle.query.filter_by(driver_id=ride.driver_id).first()
        if vehicle:
            vehicle.status = 'available'
    db.session.commit()
    return jsonify({'success': True, 'message': 'Ride cancelled'})

def simulate_ride(ride_id):
    """Simulate GPS updates for a ride"""
    ride = Ride.query.get(ride_id)
    if not ride:
        return
    route = interpolate_route(ride.pickup_lat, ride.pickup_lon, ride.dropoff_lat, ride.dropoff_lon, num_points=100)
    for i, (lat, lon) in enumerate(route):
        time.sleep(0.5)
        ride = Ride.query.get(ride_id)
        if not ride or ride.status != 'in_progress':
            break
        progress = (i / len(route)) * 100
        vehicle = Vehicle.query.filter_by(driver_id=ride.driver_id).first()
        vehicle_id = vehicle.vehicle_number if vehicle else f'RIDE-{ride_id}'
        gps_data = {
            'ride_id': ride_id,
            'vehicle_id': vehicle_id,
            'vehicle_status': vehicle.status if vehicle else 'busy',
            'latitude': lat,
            'longitude': lon,
            'progress': progress,
            'timestamp': datetime.now().isoformat()
        }
        if vehicle:
            vehicle.current_lat = lat
            vehicle.current_lon = lon
            db.session.commit()
        socketio.emit('gps_update', gps_data, room=f'ride_{ride_id}')
        socketio.emit('gps_update', gps_data, room='admins')

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    if current_user.is_authenticated:
        if current_user.role == 'driver':
            join_room('drivers')
        elif current_user.role == 'customer':
            join_room(f'customer_{current_user.id}')
        elif current_user.role == 'admin':
            join_room('admins')
    emit('connected', {'data': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

@socketio.on('join_ride')
def handle_join_ride(data):
    ride_id = data.get('ride_id')
    if ride_id:
        join_room(f'ride_{ride_id}')
        emit('joined_ride', {'ride_id': ride_id})

@socketio.on('leave_ride')
def handle_leave_ride(data):
    ride_id = data.get('ride_id')
    if ride_id:
        leave_room(f'ride_{ride_id}')
        emit('left_ride', {'ride_id': ride_id})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    start_vehicle_movement_thread()
    print("\n" + "="*80)
    print("GPS VEHICLE TRACKING - ROLE-BASED ACCESS")
    print("="*80)
    print("\nServer: http://localhost:5001")
    print("="*80 + "\n")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
