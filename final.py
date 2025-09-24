from pymongo import MongoClient
from geopy.geocoders import Nominatim
from sklearn.neighbors import NearestNeighbors
import numpy as np
import socket


# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="myGeocoder", timeout=10)
geolocator.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}



def address_to_coordinates(address):
    # Geocode the address
    location = geolocator.geocode(address)
    # Extract latitude and longitude from the geocode result
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None
    

def coordinates_to_address(latitude, longitude):
    # Reverse geocode the coordinates
    location = geolocator.reverse((latitude, longitude))

    # Extract address from the reverse geocode result
    if location:
        address = location.address
        return address
    else:
        return None

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['shehacks']  # Replace 'your_database' with your actual database name
collection = db['driver']

data = []  # List to store data from MongoDB

for doc in collection.find():
    latitude = doc['slati']
    longitude = doc['slong']
    latitude1 = doc['dlati']
    longitude1 = doc['dlong']
    time = doc['time']
    bin = doc['bin']
    
    # Append data to the list
    data.append([latitude, longitude, latitude1, longitude1, time, bin])

# Convert data to numpy array
data = np.array(data)

# Create a Nearest Neighbors model
k = 2
model = NearestNeighbors(n_neighbors=k)
model.fit(data[:, :-1])  # Fit model with all features except the preference (last column)

# Function to find nearest neighbors based on input features and filter by preferred vehicle
# Function to find nearest neighbors based on input features and filter by preferred vehicle
def find_matches(input_features, preferred_vehicle):
    distances, indices = model.kneighbors([input_features])
    nearest_indices = indices[0]
    
    # Filter by preferred vehicle
    filtered_indices = [idx for idx in nearest_indices if data[idx][-1] == preferred_vehicle]
    
    return filtered_indices

# Example usage:
global start_address
global destination_address
client = MongoClient('mongodb://localhost:27017/')
db = client['shehacks']
collection = db['passenger']

# Fetch data from MongoDB
user_data = collection.find_one(sort=[('_id', -1)])
if user_data:
    start_address = user_data['from']
    destination_address = user_data['to']
else:
    print("User data not found in MongoDB.")
    exit()

start_coordinates = address_to_coordinates(start_address)
destination_coordinates = address_to_coordinates(destination_address)
print("Start Coordinates:", start_coordinates)
print("Destination Coordinates:", destination_coordinates)


if start_coordinates and destination_coordinates:
    print("Start Coordinates:", start_coordinates)
    print("Destination Coordinates:", destination_coordinates)

    # Example input features (using coordinates instead of API)
    input_features = [start_coordinates[0], start_coordinates[1], destination_coordinates[0], destination_coordinates[1], 6]

    # Find nearest rides for the person with the given preference
    preferred_vehicle = 0  # 0 for two-wheeler, 1 for four-wheeler
    nearest_indices = find_matches(input_features, preferred_vehicle)

    if nearest_indices:
        nearest_ride = data[nearest_indices[0]]  # Get the first best ride
        print("\nNearest ride for the person with the preferred vehicle:",nearest_ride)
        
        # Fetch IP address associated with the nearest ride
        
        for doc in collection.find({'slati': nearest_ride[0], 'slong': nearest_ride[1]}):
            ip_address = doc['IP']
            print("IP Address associated with the nearest ride:", ip_address)
            
        # Convert coordinates back to addresses in English
        start_address1 = coordinates_to_address(nearest_ride[0], nearest_ride[1])
        destination_address1 = coordinates_to_address(nearest_ride[2], nearest_ride[3])
        print("\nConverted Addresses (in English):")
        print("Start Address:", start_address1)
        print("Destination Address:", destination_address1)
    else:
        print("No rides found for the specified preference.")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.239.219', 12345)

    server_socket.bind(server_address)
    server_socket.listen(1)

    print('Server listening on {}:{}'.format(*server_address))
    vclink="https://meet.google.com/xat-rqyw-zpw"

    while True:
        connection, client_address = server_socket.accept()
        try:
            print('Connection from', client_address)

            # Send a message to the client
            message_to_client = "Bhavika wants to join your ride from {} to {} link={}".format(start_address, destination_address,vclink)

            connection.sendall(message_to_client.encode())

        finally:
            connection.close()

if __name__ == "__main__":
    start_server()
