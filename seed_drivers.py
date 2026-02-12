"""
Seed missing drivers and ensure vehicle locations exist.
"""

from app_complete import app, db
from models import User, Vehicle
from city_config import BANGALORE_CONFIG, BANGALORE_VEHICLES
import random


def get_random_city_location(city):
    if city == "porto":
        # Default to bangalore center if city is unknown in this context
        center = BANGALORE_CONFIG["center"]
        return center["lat"], center["lon"]

    locations = list(BANGALORE_CONFIG["locations"].values())
    pick = random.choice(locations)
    return pick["lat"], pick["lon"]


def seed_drivers():
    with app.app_context():
        existing_vehicle_numbers = {v.vehicle_number for v in Vehicle.query.all()}
        available_vehicle_data = [
            v for v in BANGALORE_VEHICLES if v["id"] not in existing_vehicle_numbers
        ]

        created_drivers = 0
        created_vehicles = 0
        updated_locations = 0

        for driver_num in range(3, 11):
            username = f"driver{driver_num}"
            driver = User.query.filter_by(username=username).first()
            if not driver:
                driver = User(
                    username=username,
                    email=f"{username}@email.com",
                    full_name=f"Driver {driver_num}",
                    phone=f"+91 98765433{10 + driver_num}",
                    role="driver",
                )
                driver.set_password("password123")
                db.session.add(driver)
                db.session.flush()
                created_drivers += 1

            vehicle = Vehicle.query.filter_by(driver_id=driver.id).first()
            if not vehicle:
                if available_vehicle_data:
                    vehicle_data = available_vehicle_data.pop(0)
                    vehicle_number = vehicle_data["id"]
                    vehicle_type = vehicle_data["type"]
                    vehicle_model = vehicle_data["model"]
                    vehicle_color = vehicle_data["color"]
                else:
                    vehicle_number = f"KA-01-{1000 + driver_num}"
                    vehicle_type = "sedan"
                    vehicle_model = "Honda City"
                    vehicle_color = "White"

                lat, lon = get_random_city_location("bangalore")
                vehicle = Vehicle(
                    driver_id=driver.id,
                    vehicle_number=vehicle_number,
                    vehicle_type=vehicle_type,
                    vehicle_model=vehicle_model,
                    vehicle_color=vehicle_color,
                    city="bangalore",
                    current_lat=lat + random.uniform(-0.01, 0.01),
                    current_lon=lon + random.uniform(-0.01, 0.01),
                    status="available",
                    rating=round(random.uniform(4.0, 5.0), 1),
                )
                db.session.add(vehicle)
                created_vehicles += 1

        for vehicle in Vehicle.query.all():
            if vehicle.current_lat is None or vehicle.current_lon is None:
                lat, lon = get_random_city_location(vehicle.city or "bangalore")
                vehicle.current_lat = lat + random.uniform(-0.01, 0.01)
                vehicle.current_lon = lon + random.uniform(-0.01, 0.01)
                updated_locations += 1

        db.session.commit()

        print("Seed completed")
        print(f"Drivers created: {created_drivers}")
        print(f"Vehicles created: {created_vehicles}")
        print(f"Vehicle locations updated: {updated_locations}")


if __name__ == "__main__":
    seed_drivers()
