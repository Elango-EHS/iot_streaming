import json
import random
import time
import threading
import logging
import asyncio
from pymodbus.server import ModbusTcpServer
from pymodbus.datastore import ModbusSlaveContext
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusTcpProtocol


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# JSON structure for device and sensor data
json_data = {
    "device": {
        "device_id": "device_bd08032771b94bdebd5d74887a5da193",
        "device_name": "Temperature_Humidity_Sensor",
        "device_type": "Sensor",
        "location": {
            "site": "Factory A",
            "room": "Production Line 3",
            "coordinates": {
                "latitude": 37.7749,
                "longitude": -122.4194
            }
        },
        "status": "active",
        "last_maintenance": "2025-02-15T10:30:00Z",
        "next_maintenance_due": "2025-08-15T10:30:00Z"
    },
    "sensor_data": {
        "timestamp": "2025-03-15T15:45:32.632056Z",
        "data": [
            {
                "sensor_id": "temp_sensor_001",
                "sensor_type": "Temperature",
                "value": 27.37,
                "unit": "C",
                "status": "normal",
                "alarm": {
                    "status": "none",
                    "thresholds": {
                        "min": 10,
                        "max": 40
                    }
                }
            },
            {
                "sensor_id": "humidity_sensor_001",
                "sensor_type": "Humidity",
                "value": 53.83,
                "unit": "%",
                "status": "normal",
                "alarm": {
                    "status": "none",
                    "thresholds": {
                        "min": 30,
                        "max": 70
                    }
                }
            }
        ]
    },
    "metadata": {
        "data_quality": "high",
        "data_source": "IoT_Device_01",
        "protocol": "HTTP",
        "data_format": "JSON"
    }
}

# Simulate the Modbus Server/PLC with memory stores for sensor data
class MyModbusStore:
    def __init__(self):
        self._registers = [0] * 100  # Initialize 100 registers

    def set_values(self, address, values):
        """ Set values to the PLC registers """
        for i, value in enumerate(values):
            self._registers[address + i] = value

    def get_values(self, address, count):
        """ Get values from the PLC registers """
        return self._registers[address:address + count]

# Function to simulate reading sensor data and sending to PLC
def generate_sensor_data():
    # Simulating reading data from sensors (Temperature & Humidity)
    temperature = random.uniform(20, 30)  # Generate a random temperature value between 20°C to 30°C
    humidity = random.uniform(30, 60)     # Generate a random humidity value between 30% to 60%

    # Add data to the JSON structure for sensor_data
    json_data['sensor_data']['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    json_data['sensor_data']['data'][0]['value'] = round(temperature, 2)
    json_data['sensor_data']['data'][1]['value'] = round(humidity, 2)

    return json_data

# Convert JSON sensor data to Modbus registers (simulating the PLC memory)
def convert_json_to_modbus_registers(json_data):
    sensor_data = json_data["sensor_data"]
    
    # Extract temperature and humidity values from the JSON
    temperature = sensor_data["data"][0]["value"]
    humidity = sensor_data["data"][1]["value"]

    # Simulate that the Modbus PLC holds these values in registers
    temperature_registers = [int(temperature * 10)]  # Multiply by 10 for precision (e.g., 273.7 becomes 2737)
    humidity_registers = [int(humidity)]  # Humidity value directly

    return temperature_registers + humidity_registers

# Modbus server function to simulate the PLC communication
async def start_modbus_server():
    store = MyModbusStore()

    # Setup the Modbus server context
    slave_context = ModbusSlaveContext(
        di=None, co=None, hr=None, ir=None
    )
    context = ModbusSlaveContext(slave_context)

    # Create the Modbus TCP server
    server = ModbusTcpServer(context, address=("localhost", 5020))

    # Continuously send sensor data to the PLC
    while True:
        # Generate new sensor data
        sensor_data = generate_sensor_data()
        print(f"Generated sensor data: {json.dumps(sensor_data, indent=4)}")

        # Convert sensor data to Modbus registers
        modbus_data = convert_json_to_modbus_registers(sensor_data)
        
        # Update the Modbus registers with the new sensor data
        store.set_values(0, modbus_data)
        print(f"Updated Modbus registers with data: {modbus_data}")

        await asyncio.sleep(5)  # Sleep for 5 seconds before updating again

if __name__ == "__main__":
    print("Starting Modbus PLC simulator...")

    # Start Modbus server in an async thread
    loop = asyncio.get_event_loop()
    loop.create_task(start_modbus_server())

    # Run the asyncio event loop
    loop.run_forever()
