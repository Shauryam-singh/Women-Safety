import requests
import json

ORS_API_KEY = '5b3ce3597851110001cf62487ea2b9edc1b443f9bac4205b634ca8e2'

def get_route_info(start_location, end_location):
    """Fetches route information from OpenRouteService API."""
    route_url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={ORS_API_KEY}&start={start_location}&end={end_location}"
    response = requests.get(route_url)
    route_data = response.json()

    print("API Response:", json.dumps(route_data, indent=2))

    if 'routes' in route_data and len(route_data['routes']) > 0:
        route_info = route_data['routes'][0]['geometry']
        duration = route_data['routes'][0]['summary']['duration']
        distance = route_data['routes'][0]['summary']['distance']

        return {
            'route': route_info,
            'duration': duration,
            'distance': distance
        }
    else:
        raise Exception("Error fetching route data: No routes found or route data is empty")

def main():
    start_location = '8.681495,49.41443'
    end_location = '8.687872,49.420318'

    try:
        route_info = get_route_info(start_location, end_location)

        print("Route Information:")
        print(f"Route Polyline: {route_info['route']}")
        print(f"Duration (seconds): {route_info['duration']}")
        print(f"Distance (meters): {route_info['distance']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
