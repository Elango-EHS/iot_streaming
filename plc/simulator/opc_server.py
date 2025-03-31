from opcua import Server, Client, ua
from datetime import datetime
import random
import time

# Create an OPC UA server instance
server = Server()

# Set endpoint URL (adjust as needed)
server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")

# Set server name
server.set_server_name("MyOPCUAServer")

# Create a new namespace
namespace_uri = "http://localhost/opcua/"
namespace_idx = server.register_namespace(namespace_uri)

# Get the Objects node (root node for all objects)
objects_node = server.get_objects_node()

# Create a new object under the Objects node
my_object = objects_node.add_object(namespace_idx, "MyObject")

# Create variables under the object
temperature_variable = my_object.add_variable(namespace_idx, "Temperature", 0.0)
humidity_variable = my_object.add_variable(namespace_idx, "Humidity", 0.0)

# Allow writing to the variables
temperature_variable.set_writable()
humidity_variable.set_writable()

# Start the server
server.start()
print("OPC UA Server started at opc.tcp://localhost:4840/freeopcua/server/")

try:
    while True:
        # Update the variables with simulated PLC data
        temperature = round(random.uniform(20, 25), 2)  # Simulate temperature (20°C to 30°C)
        humidity = round(random.uniform(30, 45), 2)     # Simulate humidity (30% to 60%)
        temperature_variable.set_value(temperature)
        humidity_variable.set_value(humidity)
        print(f"Updated OPC UA server with Temperature={temperature}°C, Humidity={humidity}%")
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Stopping server...")
    server.stop()
    print("Server stopped.")

# OPC UA Client Configuration
OPC_SERVER_URL = "opc.tcp://localhost:4840"  # Replace with your OPC UA server URL

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
        namespace_index = client.get_namespace_index("MyNamespace")  # Replace "MyNamespace" with your namespace name
        print(f"Namespace index for 'MyNamespace': {namespace_index}")

        # Access the "MyObject" node
        try:
            my_object_node = objects.get_child([f"{namespace_index}:MyObject"])
            print(f"MyObject node: {my_object_node}")
        except Exception as e:
            print(f"Error accessing 'MyObject' node: {e}")
            return

        # Browse children of "MyObject" to find Temperature and Humidity nodes
        print("Browsing children of MyObject:")
        for child in my_object_node.get_children():
            print(f"Child: {child}, BrowseName: {child.get_browse_name()}")

        # Assume the server has nodes for temperature and humidity under "MyObject"
        try:
            temperature_node = my_object_node.get_child([f"{namespace_index}:Temperature"])
            humidity_node = my_object_node.get_child([f"{namespace_index}:Humidity"])
            print(f"Temperature node: {temperature_node}")
            print(f"Humidity node: {humidity_node}")
        except Exception as e:
            print(f"Error accessing Temperature or Humidity nodes: {e}")
            return

        # Continuously send data to the OPC UA server
        while True:
            # Generate simulated PLC data
            temperature = round(random.uniform(20, 30), 2)  # Simulate temperature (20°C to 30°C)
            humidity = round(random.uniform(30, 60), 2)     # Simulate humidity (30% to 60%)
            print(f"Sending data to OPC UA server: Temperature={temperature}°C, Humidity={humidity}%")

            # Write data to the OPC UA server nodes
            temperature_node.set_value(ua.Variant(temperature, ua.VariantType.Float))
            humidity_node.set_value(ua.Variant(humidity, ua.VariantType.Float))

            # Wait for a short interval before sending the next update
            time.sleep(0.01)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Disconnect from the OPC UA server
        client.disconnect()
        print("Disconnected from OPC UA server.")

if __name__ == "__main__":
    send_data_to_opc_server()
