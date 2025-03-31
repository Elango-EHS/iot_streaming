from opcua import Client, ua
import random
import time

# OPC UA Server Configuration
OPC_SERVER_URL = "opc.tcp://localhost:4840"  # Replace with your OPC UA server URL

# Function to simulate PLC data
def generate_plc_data():
    temperature = round(random.uniform(20, 30), 2)  # Simulate temperature (20°C to 30°C)
    humidity = round(random.uniform(30, 60), 2)     # Simulate humidity (30% to 60%)
    return temperature, humidity

def send_data_to_opc_server():
    # Connect to the OPC UA server
    client = Client(OPC_SERVER_URL)
    try:
        print(f"Connecting to OPC UA server at {OPC_SERVER_URL}...")
        client.connect()
        print("Connected to OPC UA server.")

        # Get the root node of the OPC UA server
        root = client.get_root_node()
        print(f"Root node: {root}")

        # Browse the objects node to find the PLC data nodes
        objects = client.get_objects_node()
        print(f"Objects node: {objects}")

        # Debug: Browse available nodes under the Objects node
        print("Browsing available nodes under the Objects node:")
        for child in objects.get_children():
            print(f"Child: {child}, BrowseName: {child.get_browse_name()}")

        # Adjust namespace index if necessary
        namespace_index = client.get_namespace_index("MyObject")  # Replace "MyObject" with your namespace name
        print(f"Namespace index for 'MyObject': {namespace_index}")

        # Access the "MyObject" node
        my_object_node = objects.get_child([f"{namespace_index}:MyObject"])
        print(f"MyObject node: {my_object_node}")

        # Browse children of "MyObject" to find Temperature and Humidity nodes
        print("Browsing children of MyObject:")
        for child in my_object_node.get_children():
            print(f"Child: {child}, BrowseName: {child.get_browse_name()}")

        # Assume the server has nodes for temperature and humidity under "MyObject"
        temperature_node = my_object_node.get_child([f"{namespace_index}:Temperature"])
        humidity_node = my_object_node.get_child([f"{namespace_index}:Humidity"])

        print(f"Temperature node: {temperature_node}")
        print(f"Humidity node: {humidity_node}")

        # Continuously send data to the OPC UA server
        while True:
            # Generate simulated PLC data
            temperature, humidity = generate_plc_data()
            print(f"Sending data to OPC UA server: Temperature={temperature}°C, Humidity={humidity}%")

            # Write data to the OPC UA server nodes
            temperature_node.set_value(ua.Variant(temperature, ua.VariantType.Float))
            humidity_node.set_value(ua.Variant(humidity, ua.VariantType.Float))

            # Wait for a short interval before sending the next update
            time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Disconnect from the OPC UA server
        client.disconnect()
        print("Disconnected from OPC UA server.")

if __name__ == "__main__":
    send_data_to_opc_server()