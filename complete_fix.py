"""
COMPLETE FIX SCRIPT - Database and Password Reset
Run this script to fix all login issues
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

def complete_setup():
    """Complete database setup and password reset"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*80)
        print("RIDESHARE PRO - COMPLETE DATABASE SETUP & FIX")
        print("="*80 + "\n")
        
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, 'instance', 'rideshare.db')
        
        # Step 1: Create database if it doesn't exist
        if not os.path.exists(db_path):
            print("📁 Database not found. Creating new database...")
            db.create_all()
            print(f"✓ Database created at: {db_path}\n")
        else:
            print(f"✓ Database found at: {db_path}\n")
            print("🔄 Ensuring all tables exist...")
            db.create_all()
            print("✓ Database tables verified\n")
        
        # Step 2: Delete all existing users to start fresh
        print("🗑️  Clearing existing users...")
        User.query.delete()
        Vehicle.query.delete()
        Ride.query.delete()
        db.session.commit()
        print("✓ Existing data cleared\n")
        
        # Step 3: Create admin user
        print("👤 Creating Admin user...")
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
        print("✓ Admin created successfully")
        print("   Username: admin")
        print("   Password: admin123\n")
        
        # Step 4: Create driver user
        print("👤 Creating Driver user...")
        driver = User(
            username='driver1',
            email='driver1@example.com',
            full_name='Rajesh Kumar',
            phone='9876543210',
            role='driver'
        )
        driver.set_password('password123')
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
        print("✓ Driver created successfully")
        print("   Username: driver1")
        print("   Password: password123")
        print("   Vehicle: KA-01-1234\n")
        
        # Step 5: Create customer user
        print("👤 Creating Customer user...")
        customer = User(
            username='customer1',
            email='customer1@example.com',
            full_name='John Doe',
            phone='9123456789',
            role='customer'
        )
        customer.set_password('password123')
        db.session.add(customer)
        db.session.commit()
        print("✓ Customer created successfully")
        print("   Username: customer1")
        print("   Password: password123\n")
        
        # Step 6: Verify all users can login
        print("🔐 Verifying passwords...")
        test_credentials = [
            ('admin', 'admin123'),
            ('driver1', 'password123'),
            ('customer1', 'password123')
        ]
        
        all_good = True
        for username, password in test_credentials:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                print(f"   ✓ {username}: Password verified")
            else:
                print(f"   ❌ {username}: Password verification FAILED!")
                all_good = False
        
        print()
        
        if all_good:
            print("="*80)
            print("✅ SETUP COMPLETED SUCCESSFULLY!")
            print("="*80 + "\n")
            
            print("🎯 You can now login with these credentials:\n")
            
            print("📱 ADMIN DASHBOARD")
            print("   URL: http://localhost:5000/login")
            print("   Username: admin")
            print("   Password: admin123\n")
            
            print("🚗 DRIVER DASHBOARD")
            print("   URL: http://localhost:5000/login")
            print("   Username: driver1")
            print("   Password: password123\n")
            
            print("👤 CUSTOMER DASHBOARD")
            print("   URL: http://localhost:5000/login")
            print("   Username: customer1")
            print("   Password: password123\n")
            
            print("="*80)
            print("💡 NEXT STEPS:")
            print("   1. Run: python app_complete.py")
            print("   2. Open: http://localhost:5000")
            print("   3. Login with any of the credentials above")
            print("="*80 + "\n")
        else:
            print("❌ SETUP COMPLETED WITH ERRORS")
            print("Please check the error messages above\n")

if __name__ == '__main__':
    try:
        complete_setup()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        print("\n⚠️  If you see SQLAlchemy errors, make sure:")
        print("   1. No other instances of app_complete.py are running")
        print("   2. The instance folder has write permissions")
        print("   3. You've activated your virtual environment\n")
        sys.exit(1)
