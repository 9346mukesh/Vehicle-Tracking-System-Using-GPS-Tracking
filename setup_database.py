"""
Database Setup Script
Run this script to initialize the database with proper structure and sample data
"""

import os
import sys
from flask import Flask
from models import db, User, Vehicle, Ride, SystemSettings
from werkzeug.security import generate_password_hash

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gps_tracking_secret_key_2026'
    
    # Get the absolute path to the database directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'rideshare.db')
    
    # Ensure instance directory exists
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    return app

def setup_database():
    """Initialize database and create sample data"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if admin already exists
        if User.query.filter_by(username='admin').first():
            print("✓ Admin user already exists")
        else:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@rideshare.com',
                full_name='System Administrator',
                phone='1234567890',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created successfully!")
            print("  Username: admin")
            print("  Password: admin123")
        
        # Create sample customer
        if not User.query.filter_by(username='customer1').first():
            print("Creating sample customer...")
            customer = User(
                username='customer1',
                email='customer1@example.com',
                full_name='John Doe',
                phone='9876543210',
                role='customer'
            )
            customer.set_password('customer123')
            db.session.add(customer)
            db.session.commit()
            print("✓ Sample customer created!")
            print("  Username: customer1")
            print("  Password: customer123")
        
        # Create sample driver
        if not User.query.filter_by(username='driver1').first():
            print("Creating sample driver...")
            driver = User(
                username='driver1',
                email='driver1@example.com',
                full_name='Rajesh Kumar',
                phone='9123456789',
                role='driver'
            )
            driver.set_password('driver123')
            db.session.add(driver)
            db.session.commit()
            
            # Create vehicle for driver
            vehicle = Vehicle(
                driver_id=driver.id,
                vehicle_number='KA-01-1234',
                vehicle_type='sedan',
                vehicle_model='Honda City',
                vehicle_color='White',
                city='bangalore',
                current_lat=12.9716,
                current_lon=77.5946,
                status='available',
                rating=4.8,
                total_trips=150
            )
            db.session.add(vehicle)
            db.session.commit()
            print("✓ Sample driver and vehicle created!")
            print("  Username: driver1")
            print("  Password: driver123")
            print("  Vehicle: KA-01-1234")
        
        # Create system settings
        if not SystemSettings.query.filter_by(key='system_status').first():
            print("Creating system settings...")
            settings = [
                SystemSettings(key='system_status', value='active', description='System operational status'),
                SystemSettings(key='max_ride_distance', value='50', description='Maximum ride distance in km'),
                SystemSettings(key='surge_multiplier', value='1.5', description='Surge pricing multiplier'),
            ]
            for setting in settings:
                db.session.add(setting)
            db.session.commit()
            print("✓ System settings created!")
        
        print("\n" + "="*80)
        print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nDatabase Location:")
        print(f"  {os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'rideshare.db')}")
        print("\nDefault Login Credentials:")
        print("\n  Admin:")
        print("    Username: admin")
        print("    Password: admin123")
        print("\n  Sample Customer:")
        print("    Username: customer1")
        print("    Password: customer123")
        print("\n  Sample Driver:")
        print("    Username: driver1")
        print("    Password: driver123")
        print("="*80 + "\n")

if __name__ == '__main__':
    try:
        setup_database()
    except Exception as e:
        print(f"\n❌ Error setting up database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
