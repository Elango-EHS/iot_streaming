import json
import random
from datetime import datetime
import uuid

# Function to generate dynamic temperature and humidity values
def generateTemprature():
    # Dynamic temperature value between 15.0 and 30.0 C
    temperature = round(random.uniform(15.0, 30.0), 2)
    return temperature
    
def generateHumidity():    # Dynamic humidity value between 30.0 and 70.0 %
    humidity = round(random.uniform(30.0, 70.0), 2)
    return humidity      
    

# Function to generate a dynamic unique device ID
def getRandomDeviceID():
    # Generate a unique device ID using UUID
    return f"device_{uuid.uuid4().hex}"

# Function to generate a dynamic timestamp
def getRandomTimestamp():
    # Get the current timestamp in milliseconds
    return int(datetime.now().timestamp() * 1000)

# Function to generate a random site name
def getRandomSiteName():
    # List of possible site names
    site_names = ["Factory A", "Factory B", "Factory C"]
    return random.choice(site_names)


def getRandomCoordinates():
    # Generate random latitude and longitude values
    latitude = round(random.uniform(-90.0, 90.0), 6)
    longitude = round(random.uniform(-180.0, 180.0), 6)
    
    return {
        "latitude": latitude,
        "longitude": longitude
    }

def getRandomRoomName():
    # List of possible room names
    room_names = ["Production Line 1", "Production Line 2", "Production Line 3"]
    return random.choice(room_names)

def getRandomStatus():
    # List of possible status values
    status_values = ["active", "inactive", "maintenance"]
    return random.choice(status_values)
    
def getRandomSensorType():
    # List of possible sensor types
    sensor_types = ["Temperature Sensor", "Humidity Sensor", "Pressure Sensor"]
    return random.choice(sensor_types)


