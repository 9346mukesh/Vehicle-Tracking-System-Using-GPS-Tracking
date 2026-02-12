"""
City Configuration - Bangalore and Porto
Contains location data, routes, and city-specific settings
"""

# Bangalore, India Configuration
BANGALORE_CONFIG = {
    'name': 'Bangalore',
    'country': 'India',
    'center': {'lat': 12.9716, 'lon': 77.5946},
    'zoom_level': 12,
    'currency': '₹',
    'base_fare': 50,  # Base fare in INR
    'per_km_rate': 12,  # Rate per kilometer
    'traffic_multiplier': {
        'rush_hour_morning': {'hours': [7, 8, 9, 10], 'multiplier': 1.8},
        'rush_hour_evening': {'hours': [17, 18, 19, 20], 'multiplier': 2.0},
        'normal': {'multiplier': 1.0},
        'late_night': {'hours': [22, 23, 0, 1, 2, 3, 4, 5], 'multiplier': 0.7}
    },
    'locations': {
        'mg_road': {
            'lat': 12.9716, 
            'lon': 77.5946, 
            'name': 'MG Road',
            'type': 'commercial'
        },
        'electronic_city': {
            'lat': 12.8456, 
            'lon': 77.6603, 
            'name': 'Electronic City',
            'type': 'tech_hub'
        },
        'whitefield': {
            'lat': 12.9698, 
            'lon': 77.7499, 
            'name': 'Whitefield',
            'type': 'tech_hub'
        },
        'koramangala': {
            'lat': 12.9352, 
            'lon': 77.6245, 
            'name': 'Koramangala',
            'type': 'residential'
        },
        'indiranagar': {
            'lat': 12.9716, 
            'lon': 77.6412, 
            'name': 'Indiranagar',
            'type': 'residential'
        },
        'jayanagar': {
            'lat': 12.9250, 
            'lon': 77.5838, 
            'name': 'Jayanagar',
            'type': 'residential'
        },
        'hsr_layout': {
            'lat': 12.9116, 
            'lon': 77.6373, 
            'name': 'HSR Layout',
            'type': 'residential'
        },
        'bannerghatta': {
            'lat': 12.8006, 
            'lon': 77.5974, 
            'name': 'Bannerghatta Road',
            'type': 'suburban'
        },
        'airport': {
            'lat': 13.1986, 
            'lon': 77.7066, 
            'name': 'Kempegowda Airport',
            'type': 'airport'
        },
        'majestic': {
            'lat': 12.9767, 
            'lon': 77.5710, 
            'name': 'Majestic',
            'type': 'transport_hub'
        },
        'btm_layout': {
            'lat': 12.9165,
            'lon': 77.6101,
            'name': 'BTM Layout',
            'type': 'residential'
        },
        'bellandur': {
            'lat': 12.9259,
            'lon': 77.6751,
            'name': 'Bellandur',
            'type': 'tech_hub'
        },
        'marathahalli': {
            'lat': 12.9591,
            'lon': 77.7011,
            'name': 'Marathahalli',
            'type': 'commercial'
        },
        'jp_nagar': {
            'lat': 12.9077,
            'lon': 77.5854,
            'name': 'JP Nagar',
            'type': 'residential'
        }
    },
    'popular_routes': [
        ('mg_road', 'electronic_city'),
        ('whitefield', 'mg_road'),
        ('koramangala', 'airport'),
        ('indiranagar', 'bannerghatta'),
        ('jayanagar', 'whitefield'),
        ('hsr_layout', 'majestic'),
        ('airport', 'koramangala'),
        ('majestic', 'electronic_city'),
        ('electronic_city', 'whitefield'),
        ('bannerghatta', 'indiranagar'),
        ('btm_layout', 'marathahalli'),
        ('bellandur', 'mg_road'),
        ('jp_nagar', 'airport'),
        ('whitefield', 'jayanagar')
    ]
}

# Porto, Portugal Configuration
PORTO_CONFIG = {
    'name': 'Porto',
    'country': 'Portugal',
    'center': {'lat': 41.1579, 'lon': -8.6291},
    'zoom_level': 13,
    'currency': '€',
    'base_fare': 3.50,  # Base fare in EUR
    'per_km_rate': 0.80,  # Rate per kilometer
    'traffic_multiplier': {
        'rush_hour_morning': {'hours': [7, 8, 9], 'multiplier': 1.5},
        'rush_hour_evening': {'hours': [17, 18, 19], 'multiplier': 1.6},
        'normal': {'multiplier': 1.0},
        'late_night': {'hours': [22, 23, 0, 1, 2, 3, 4, 5], 'multiplier': 0.8}
    },
    'locations': {
        'city_center': {
            'lat': 41.1579,
            'lon': -8.6291,
            'name': 'City Center',
            'type': 'commercial'
        },
        'beach': {
            'lat': 41.1496,
            'lon': -8.6109,
            'name': 'Beach',
            'type': 'tourist'
        },
        'airport': {
            'lat': 41.2481,
            'lon': -8.6814,
            'name': 'Francisco Sá Carneiro Airport',
            'type': 'airport'
        },
        'downtown': {
            'lat': 41.1621,
            'lon': -8.6531,
            'name': 'Downtown',
            'type': 'commercial'
        },
        'university': {
            'lat': 41.1773,
            'lon': -8.5960,
            'name': 'University',
            'type': 'education'
        },
        'hospital': {
            'lat': 41.1579,
            'lon': -8.6291,
            'name': 'Hospital',
            'type': 'medical'
        },
        'boavista': {
            'lat': 41.1579,
            'lon': -8.6500,
            'name': 'Boavista',
            'type': 'commercial'
        },
        'matosinhos': {
            'lat': 41.1820,
            'lon': -8.6900,
            'name': 'Matosinhos',
            'type': 'coastal'
        }
    },
    'popular_routes': [
        ('city_center', 'beach'),
        ('airport', 'downtown'),
        ('university', 'hospital'),
        ('downtown', 'beach'),
        ('airport', 'city_center'),
        ('boavista', 'matosinhos'),
        ('university', 'downtown'),
        ('beach', 'city_center')
    ]
}

# Default vehicles for each city
BANGALORE_VEHICLES = [
    {'id': 'KA-01-1000', 'type': 'sedan', 'model': 'Honda City', 'color': 'White'},
    {'id': 'KA-01-1001', 'type': 'suv', 'model': 'Toyota Innova', 'color': 'Silver'},
    {'id': 'KA-01-1002', 'type': 'sedan', 'model': 'Maruti Dzire', 'color': 'Blue'},
    {'id': 'KA-01-1003', 'type': 'sedan', 'model': 'Hyundai Verna', 'color': 'Black'},
    {'id': 'KA-01-1004', 'type': 'suv', 'model': 'Mahindra XUV', 'color': 'Red'},
    {'id': 'KA-01-1005', 'type': 'sedan', 'model': 'Honda City', 'color': 'Grey'},
    {'id': 'KA-01-1006', 'type': 'sedan', 'model': 'Volkswagen Vento', 'color': 'White'},
    {'id': 'KA-01-1007', 'type': 'suv', 'model': 'Toyota Fortuner', 'color': 'Black'},
    {'id': 'KA-01-1008', 'type': 'sedan', 'model': 'Skoda Rapid', 'color': 'Silver'},
    {'id': 'KA-01-1009', 'type': 'suv', 'model': 'Kia Seltos', 'color': 'White'}
]

PORTO_VEHICLES = [
    {'id': 'PO-01-AA-1000', 'type': 'sedan', 'model': 'Mercedes E-Class', 'color': 'Black'},
    {'id': 'PO-01-AA-1001', 'type': 'sedan', 'model': 'BMW 3 Series', 'color': 'White'},
    {'id': 'PO-01-AA-1002', 'type': 'sedan', 'model': 'Audi A4', 'color': 'Silver'},
    {'id': 'PO-01-AA-1003', 'type': 'sedan', 'model': 'VW Passat', 'color': 'Blue'},
    {'id': 'PO-01-AA-1004', 'type': 'suv', 'model': 'BMW X5', 'color': 'Black'},
    {'id': 'PO-01-AA-1005', 'type': 'sedan', 'model': 'Mercedes C-Class', 'color': 'Grey'},
    {'id': 'PO-01-AA-1006', 'type': 'sedan', 'model': 'Audi A6', 'color': 'White'},
    {'id': 'PO-01-AA-1007', 'type': 'suv', 'model': 'Volvo XC90', 'color': 'Black'},
    {'id': 'PO-01-AA-1008', 'type': 'sedan', 'model': 'BMW 5 Series', 'color': 'Silver'},
    {'id': 'PO-01-AA-1009', 'type': 'sedan', 'model': 'Mercedes S-Class', 'color': 'Black'}
]

def get_city_config(city_name):
    """Get configuration for a specific city"""
    if city_name.lower() == 'bangalore':
        return BANGALORE_CONFIG
    elif city_name.lower() == 'porto':
        return PORTO_CONFIG
    else:
        return BANGALORE_CONFIG  # Default to Bangalore

def get_vehicles_for_city(city_name):
    """Get default vehicles for a specific city"""
    if city_name.lower() == 'bangalore':
        return BANGALORE_VEHICLES
    elif city_name.lower() == 'porto':
        return PORTO_VEHICLES
    else:
        return BANGALORE_VEHICLES

def calculate_fare(distance_km, city_name, hour=None):
    """Calculate fare based on distance and city"""
    config = get_city_config(city_name)
    
    base_fare = config['base_fare']
    per_km = config['per_km_rate']
    
    # Calculate base fare
    fare = base_fare + (distance_km * per_km)
    
    # Apply traffic multiplier if hour is provided
    if hour is not None:
        traffic = config['traffic_multiplier']
        if hour in traffic['rush_hour_morning']['hours']:
            fare *= traffic['rush_hour_morning']['multiplier']
        elif hour in traffic['rush_hour_evening']['hours']:
            fare *= traffic['rush_hour_evening']['multiplier']
        elif hour in traffic['late_night']['hours']:
            fare *= traffic['late_night']['multiplier']
    
    return round(fare, 2)

def get_location_by_name(city_name, location_name):
    """Get location details by name"""
    config = get_city_config(city_name)
    return config['locations'].get(location_name)

def get_all_locations(city_name):
    """Get all locations for a city"""
    config = get_city_config(city_name)
    return config['locations']
