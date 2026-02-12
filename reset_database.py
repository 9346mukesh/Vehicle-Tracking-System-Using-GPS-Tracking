"""
COMPLETE DATABASE RESET SCRIPT
This will delete and recreate the database with proper credentials
Run this if login is not working
"""

import os
from app_complete import app, db
from models import User, Vehicle, Ride, SystemSettings
from datetime import datetime, timedelta
import random

def reset_database():
    """Complete database reset"""
    with app.app_context():
        print("\n" + "="*80)
        print("COMPLETE DATABASE RESET")
        print("="*80)
        
        # Delete existing database file
        db_path = 'instance/rideshare.db'
        if os.path.exists(db_path):
            print(f"\n✓ Deleting existing database: {db_path}")
            os.remove(db_path)
        
        # Create fresh database
        print("✓ Creating fresh database tables...")
        db.create_all()
        
        # ============================================
        # CREATE ADMIN USER
        # ============================================
        print("\n" + "-"*80)
        print("CREATING ADMIN USER")
        print("-"*80)
        
        admin = User(
            username='admin',
            email='admin@rideshare.com',
            full_name='System Administrator',
            phone='+91 9876543210',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()
        
        # Verify password immediately
        if admin.check_password('admin123'):
            print("✓ Admin user created successfully")
            print(f"  Username: admin")
            print(f"  Password: admin123")
            print(f"  Password verification: PASSED ✓")
        else:
            print("✗ ERROR: Admin password verification FAILED!")
        
        # ============================================
        # CREATE CUSTOMER USERS
        # ============================================
        print("\n" + "-"*80)
        print("CREATING CUSTOMER USERS")
        print("-"*80)
        
        customers = []
        for i in range(1, 6):
            customer = User(
                username=f'customer{i}',
                email=f'customer{i}@email.com',
                full_name=f'Customer User {i}',
                phone=f'+91 98765432{10+i}',
                role='customer'
            )
            customer.set_password('password123')
            customers.append(customer)
            db.session.add(customer)
            db.session.flush()
            
            # Verify password
            if customer.check_password('password123'):
                print(f"✓ customer{i} created - Password verification: PASSED ✓")
            else:
                print(f"✗ ERROR: customer{i} password verification FAILED!")
        
        # ============================================
        # CREATE DRIVER USERS WITH VEHICLES
        # ============================================
        print("\n" + "-"*80)
        print("CREATING DRIVER USERS & VEHICLES")
        print("-"*80)
        
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
            db.session.flush()
            
            # Verify password
            if driver.check_password('password123'):
                print(f"✓ driver{i} created - Password verification: PASSED ✓")
            else:
                print(f"✗ ERROR: driver{i} password verification FAILED!")
            
            # Create vehicle
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
            print(f"  └─ Vehicle: {veh_data['number']} - {veh_data['model']}")
        
        # Commit all users
        db.session.commit()
        
        # ============================================
        # CREATE SAMPLE RIDES
        # ============================================
        print("\n" + "-"*80)
        print("CREATING SAMPLE RIDE HISTORY")
        print("-"*80)
        
        statuses = ['completed', 'completed', 'completed', 'cancelled']
        
        for i in range(20):
            customer = random.choice(customers)
            driver = random.choice(drivers)
            
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
                pickup_address=f'Bangalore Location {i}A',
                dropoff_lat=dropoff_lat,
                dropoff_lon=dropoff_lon,
                dropoff_address=f'Bangalore Location {i}B',
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
        
        print(f"✓ Created 20 sample rides")
        
        # ============================================
        # CREATE SYSTEM SETTINGS
        # ============================================
        print("\n" + "-"*80)
        print("CREATING SYSTEM SETTINGS")
        print("-"*80)
        
        settings = [
            SystemSettings(key='base_fare_bangalore', value='50', description='Base fare for Bangalore in INR'),
            SystemSettings(key='base_fare_porto', value='3.50', description='Base fare for Porto in EUR'),
            SystemSettings(key='per_km_rate_bangalore', value='12', description='Per km rate for Bangalore in INR'),
            SystemSettings(key='per_km_rate_porto', value='0.80', description='Per km rate for Porto in EUR'),
        ]
        
        for setting in settings:
            db.session.add(setting)
        
        print(f"✓ Created {len(settings)} system settings")
        
        # Final commit
        db.session.commit()
        
        # ============================================
        # FINAL VERIFICATION
        # ============================================
        print("\n" + "="*80)
        print("FINAL VERIFICATION - TESTING LOGIN CREDENTIALS")
        print("="*80)
        
        test_credentials = [
            ('admin', 'admin123'),
            ('driver1', 'password123'),
            ('driver2', 'password123'),
            ('customer1', 'password123'),
            ('customer2', 'password123'),
        ]
        
        all_passed = True
        for username, password in test_credentials:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                print(f"✓ {username:12} | Password: {password:15} | Verification: PASSED ✓")
            else:
                print(f"✗ {username:12} | Password: {password:15} | Verification: FAILED ✗")
                all_passed = False
        
        # ============================================
        # SUMMARY
        # ============================================
        print("\n" + "="*80)
        print("DATABASE RESET COMPLETE!")
        print("="*80)
        print(f"\nTotal Users: {User.query.count()}")
        print(f"Total Vehicles: {Vehicle.query.count()}")
        print(f"Total Rides: {Ride.query.count()}")
        print(f"Total Settings: {SystemSettings.query.count()}")
        
        if all_passed:
            print("\n✓✓✓ ALL LOGIN CREDENTIALS VERIFIED AND WORKING! ✓✓✓")
        else:
            print("\n✗✗✗ SOME CREDENTIALS FAILED VERIFICATION! ✗✗✗")
        
        print("\n" + "-"*80)
        print("LOGIN CREDENTIALS TO USE:")
        print("-"*80)
        print("\nADMIN LOGIN:")
        print("  URL: http://localhost:5000/login")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nDRIVER LOGIN:")
        print("  Username: driver1 (or driver2, driver3, driver4, driver5)")
        print("  Password: password123")
        print("\nCUSTOMER LOGIN:")
        print("  Username: customer1 (or customer2, customer3, customer4, customer5)")
        print("  Password: password123")
        print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    reset_database()
