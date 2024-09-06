from geopy.distance import great_circle

SAFE_ZONE_CENTER = (77.3300, 77.3300)
SAFE_ZONE_RADIUS = 1000  

def is_within_safe_zone(current_location):
    """Check if the current location is within the safe zone."""
    distance = great_circle(SAFE_ZONE_CENTER, current_location).meters
    return distance <= SAFE_ZONE_RADIUS

def check_geofencing(current_lat, current_lon):
    """Check if user is within the safe zone and send alert if not."""
    current_location = (current_lat, current_lon)
    if not is_within_safe_zone(current_location):
        message = f"Alert! You have exited the safe zone. Coordinates: ({current_lat}, {current_lon})"
        print("Geofence alert sent.")
    else:
        print("You are within the safe zone.")

def main():
    current_lat = 28.5800
    current_lon = 77.3300

    try:
        check_geofencing(current_lat, current_lon)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
