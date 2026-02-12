"""
Quick Database Check Script
Verifies users and their passwords
"""

from app_complete import app, db
from models import User, Vehicle, Ride

def check_database():
    """Check database contents"""
    with app.app_context():
        print("\n" + "="*80)
        print("DATABASE CHECK")
        print("="*80)
        
        # Count records
        user_count = User.query.count()
        vehicle_count = Vehicle.query.count()
        ride_count = Ride.query.count()
        
        print(f"\nTotal Users: {user_count}")
        print(f"Total Vehicles: {vehicle_count}")
        print(f"Total Rides: {ride_count}")
        
        # Check specific users
        print("\n" + "-"*80)
        print("USER DETAILS:")
        print("-"*80)
        
        test_users = ['admin', 'driver1', 'customer1']
        test_password = {
            'admin': 'admin123',
            'driver1': 'password123',
            'customer1': 'password123'
        }
        
        for username in test_users:
            user = User.query.filter_by(username=username).first()
            if user:
                # Test password
                password_valid = user.check_password(test_password[username])
                print(f"\n✓ Username: {username}")
                print(f"  - Role: {user.role}")
                print(f"  - Email: {user.email}")
                print(f"  - Full Name: {user.full_name}")
                print(f"  - Password Check: {'✓ VALID' if password_valid else '✗ INVALID'}")
                print(f"  - Password Hash: {user.password_hash[:50]}...")
            else:
                print(f"\n✗ User '{username}' NOT FOUND")
        
        # List all users
        print("\n" + "-"*80)
        print("ALL USERS IN DATABASE:")
        print("-"*80)
        all_users = User.query.all()
        for user in all_users:
            print(f"  {user.username:15} | Role: {user.role:10} | Email: {user.email}")
        
        print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    check_database()
