"""
Database Initialization Script
Creates tables and populates with sample data
"""

from app_complete import app, db
from models import User, Vehicle, Ride, SystemSettings
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with complete sample data"""
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating tables...")
        db.create_all()
        
        # Create Admin User
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@rideshare.com',
            full_name='System Administrator',
            phone='+91 9876543210',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create Sample Customers
        print("Creating sample customers...")
        customers = []
        for i in range(1, 6):
            customer = User(
                username=f'customer{i}',
                email=f'customer{i}@email.com',
                full_name=f'Customer {i}',
                phone=f'+91 98765432{10+i}',
                role='customer'
            )
            customer.set_password('password123')
            customers.append(customer)
            db.session.add(customer)
        
        # Create Sample Drivers with Vehicles
        print("Creating sample drivers and vehicles...")
        drivers = []
        bangalore_vehicles = [
            {'number': 'KA-01-1000', 'type': 'sedan', 'model': 'Honda City', 'color': 'White'},
            {'number': 'KA-01-1001', 'type': 'suv', 'model': 'Toyota Innova', 'color': 'Silver'},
            {'number': 'KA-01-1002', 'type': 'sedan', 'model': 'Maruti Dzire', 'color': 'Blue'},
            {'number': 'KA-01-1003', 'type': 'sedan', 'model': 'Hyundai Verna', 'color': 'Black'},
            {'number': 'KA-01-1004', 'type': 'suv', 'model': 'Mahindra XUV', 'color': 'Red'},
        ]
        
        for i, veh_data in enumerate(bangalore_vehicles, 1):
            driver = User(
                username=f'driver{i}',
                email=f'driver{i}@email.com',
                full_name=f'Driver {i}',
                phone=f'+91 98765433{10+i}',
                role='driver'
            )
            driver.set_password('password123')
            drivers.append(driver)
            db.session.add(driver)
            db.session.flush()  # Get driver ID
            
            vehicle = Vehicle(
                driver_id=driver.id,
                vehicle_number=veh_data['number'],
                vehicle_type=veh_data['type'],
                vehicle_model=veh_data['model'],
                vehicle_color=veh_data['color'],
                city='bangalore',
                current_lat=12.9716 + random.uniform(-0.05, 0.05),
                current_lon=77.5946 + random.uniform(-0.05, 0.05),
                status='available',
                rating=round(random.uniform(4.0, 5.0), 1),
                total_trips=random.randint(50, 300)
            )
            db.session.add(vehicle)
        
        db.session.commit()
        
        # Create Sample Rides
        print("Creating sample ride history...")
        statuses = ['completed', 'completed', 'completed', 'cancelled']
        
        for i in range(20):
            customer = random.choice(customers)
            driver = random.choice(drivers)
            
            # Random locations
            pickup_lat = 12.9716 + random.uniform(-0.1, 0.1)
            pickup_lon = 77.5946 + random.uniform(-0.1, 0.1)
            dropoff_lat = 12.9716 + random.uniform(-0.1, 0.1)
            dropoff_lon = 77.5946 + random.uniform(-0.1, 0.1)
            
            distance = random.uniform(5, 25)
            duration = distance * random.uniform(3, 6)
            fare = 50 + (distance * 12)
            
            created_time = datetime.utcnow() - timedelta(days=random.randint(0, 30))
            
            ride = Ride(
                customer_id=customer.id,
                driver_id=driver.id,
                pickup_lat=pickup_lat,
                pickup_lon=pickup_lon,
                pickup_address=f'Location {i}A',
                dropoff_lat=dropoff_lat,
                dropoff_lon=dropoff_lon,
                dropoff_address=f'Location {i}B',
                city='bangalore',
                distance=distance,
                duration=duration,
                fare=round(fare, 2),
                status=random.choice(statuses),
                created_at=created_time,
                accepted_at=created_time + timedelta(minutes=2),
                started_at=created_time + timedelta(minutes=5),
                completed_at=created_time + timedelta(minutes=5+duration) if random.choice(statuses) == 'completed' else None,
                rating=round(random.uniform(3.5, 5.0), 1) if random.choice(statuses) == 'completed' else None
            )
            db.session.add(ride)
        
        db.session.commit()
        
        # Create System Settings
        print("Creating system settings...")
        settings = [
            SystemSettings(key='base_fare_bangalore', value='50', description='Base fare for Bangalore in INR'),
            SystemSettings(key='base_fare_porto', value='3.50', description='Base fare for Porto in EUR'),
            SystemSettings(key='per_km_rate_bangalore', value='12', description='Per km rate for Bangalore in INR'),
            SystemSettings(key='per_km_rate_porto', value='0.80', description='Per km rate for Porto in EUR'),
        ]
        
        for setting in settings:
            db.session.add(setting)
        
        db.session.commit()
        
        print("\n" + "="*80)
        print("DATABASE INITIALIZED SUCCESSFULLY!")
        print("="*80)
        print("\nCreated Users:")
        print("  Admin:")
        print("    Username: admin | Password: admin123")
        print("\n  Customers:")
        for i in range(1, 6):
            print(f"    Username: customer{i} | Password: password123")
        print("\n  Drivers:")
        for i in range(1, 6):
            print(f"    Username: driver{i} | Password: password123")
        print("\n  Sample Rides: 20 rides created")
        print("  Sample Vehicles: 5 vehicles in Bangalore")
        print("="*80 + "\n")

if __name__ == '__main__':
    init_database()
