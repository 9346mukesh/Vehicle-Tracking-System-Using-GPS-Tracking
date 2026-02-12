"""
Initialize Database and Create Sample Data
"""

from app import app, db
from models import User, Vehicle, Ride
from city_config import get_vehicles_for_city, BANGALORE_CONFIG, PORTO_CONFIG
from datetime import datetime
import random

def init_database():
    """Initialize database and create tables"""
    with app.app_context():
        # Drop all tables and recreate (WARNING: This deletes all data!)
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print("✓ Admin user already exists")
            return
        
        # Create admin user
        print("\nCreating users...")
        admin = User(
            username='admin',
            email='admin@rideshare.com',
            role='admin',
            full_name='System Administrator',
            phone='+91-9876543210'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample drivers for Bangalore
        bangalore_drivers = []
        bangalore_vehicles_data = get_vehicles_for_city('bangalore')
        
        for i, vehicle_data in enumerate(bangalore_vehicles_data):
            driver = User(
                username=f'driver_blr_{i+1}',
                email=f'driver{i+1}@bangalore.com',
                role='driver',
                full_name=f'Driver {i+1} Bangalore',
                phone=f'+91-98765432{10+i}'
            )
            driver.set_password('driver123')
            db.session.add(driver)
            bangalore_drivers.append(driver)
        
        # Create sample drivers for Porto
        porto_drivers = []
        porto_vehicles_data = get_vehicles_for_city('porto')
        
        for i, vehicle_data in enumerate(porto_vehicles_data):
            driver = User(
                username=f'driver_porto_{i+1}',
                email=f'driver{i+1}@porto.com',
                role='driver',
                full_name=f'Driver {i+1} Porto',
                phone=f'+351-91234567{i}'
            )
            driver.set_password('driver123')
            db.session.add(driver)
            porto_drivers.append(driver)
        
        # Create sample customers
        customers = []
        for i in range(5):
            customer = User(
                username=f'customer_{i+1}',
                email=f'customer{i+1}@example.com',
                role='customer',
                full_name=f'Customer {i+1}',
                phone=f'+91-98765{10000+i}'
            )
            customer.set_password('customer123')
            db.session.add(customer)
            customers.append(customer)
        
        db.session.commit()
        print(f"✓ Created {len(bangalore_drivers)} Bangalore drivers")
        print(f"✓ Created {len(porto_drivers)} Porto drivers")
        print(f"✓ Created {len(customers)} customers")
        print("✓ Created 1 admin user")
        
        # Create vehicles for Bangalore drivers
        print("\nCreating vehicles...")
        bangalore_locations = list(BANGALORE_CONFIG['locations'].values())
        
        for i, driver in enumerate(bangalore_drivers):
            vehicle_data = bangalore_vehicles_data[i]
            random_location = random.choice(bangalore_locations)
            
            vehicle = Vehicle(
                driver_id=driver.id,
                vehicle_number=vehicle_data['id'],
                vehicle_type=vehicle_data['type'],
                vehicle_model=vehicle_data['model'],
                vehicle_color=vehicle_data['color'],
                city='bangalore',
                current_lat=random_location['lat'] + random.uniform(-0.01, 0.01),
                current_lon=random_location['lon'] + random.uniform(-0.01, 0.01),
                status='available',
                rating=round(random.uniform(4.5, 5.0), 1)
            )
            db.session.add(vehicle)
        
        # Create vehicles for Porto drivers
        porto_locations = list(PORTO_CONFIG['locations'].values())
        
        for i, driver in enumerate(porto_drivers):
            vehicle_data = porto_vehicles_data[i]
            random_location = random.choice(porto_locations)
            
            vehicle = Vehicle(
                driver_id=driver.id,
                vehicle_number=vehicle_data['id'],
                vehicle_type=vehicle_data['type'],
                vehicle_model=vehicle_data['model'],
                vehicle_color=vehicle_data['color'],
                city='porto',
                current_lat=random_location['lat'] + random.uniform(-0.01, 0.01),
                current_lon=random_location['lon'] + random.uniform(-0.01, 0.01),
                status='available',
                rating=round(random.uniform(4.5, 5.0), 1)
            )
            db.session.add(vehicle)
        
        db.session.commit()
        print(f"✓ Created {len(bangalore_drivers)} Bangalore vehicles")
        print(f"✓ Created {len(porto_drivers)} Porto vehicles")
        
        print("\n" + "="*60)
        print("DATABASE INITIALIZED SUCCESSFULLY!")
        print("="*60)
        print("\nDefault Login Credentials:")
        print("-" * 60)
        print("ADMIN:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nDRIVERS (Bangalore):")
        print("  Username: driver_blr_1 to driver_blr_10")
        print("  Password: driver123")
        print("\nDRIVERS (Porto):")
        print("  Username: driver_porto_1 to driver_porto_10")
        print("  Password: driver123")
        print("\nCUSTOMERS:")
        print("  Username: customer_1 to customer_5")
        print("  Password: customer123")
        print("="*60)

if __name__ == '__main__':
    init_database()
