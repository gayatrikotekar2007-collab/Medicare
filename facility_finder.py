from database import get_db
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    # Simple distance calculation (for demonstration)
    # In a real application, you would use a more accurate method
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

def get_nearby_facilities(location, facility_type):
    db = get_db()
    
    # For simplicity, we'll use fixed coordinates as the user's location
    user_lat, user_lon = 40.7128, -74.0060  # New York coordinates
    
    facilities = db.execute('SELECT * FROM medical_facilities').fetchall()
    
    results = []
    for facility in facilities:
        # Skip if facility type doesn't match filter
        if facility_type and facility['type'] != facility_type:
            continue
            
        # Calculate distance (simplified)
        dist = calculate_distance(user_lat, user_lon, facility['latitude'], facility['longitude'])
        
        # Convert to miles (very approximate)
        miles = dist * 69
        
        results.append({
            'id': facility['id'],
            'name': facility['name'],
            'type': facility['type'],
            'address': facility['address'],
            'city': facility['city'],
            'phone': facility['phone'],
            'distance': round(miles, 1)
        })
    
    # Sort by distance
    results.sort(key=lambda x: x['distance'])
    return results