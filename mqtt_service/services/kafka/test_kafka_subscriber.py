import base64
import json
import time
from confluent_kafka import Consumer, KafkaException, KafkaError
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuration for Kafka Consumer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'my_consumer_group',        # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start consuming from the earliest message
}

# Create Kafka consumer instance
consumer = Consumer(conf)

# The topic you want to consume messages from
topic = 'test-iot-topic'

# Subscribe to the topic
consumer.subscribe([topic])
print('Poll for new messages')

# Configuration for InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "mvmKmiT_b6hNSEvEYZKT2dhqnVsSq5mXoDsztOwrESzcOs6Fr5xpAO6hxZoeH4nW_0Ttvr46pAKkc4dppuSNAQ=="
influxdb_org = "ehs"
influxdb_bucket = "iot"

# Initialize InfluxDB client
influx_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Timeout in seconds

        if msg is None:
            print('No Messages Received')
            continue
        if msg.error():
            # Handle errors
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"End of partition reached {msg.topic()} [{msg.partition}] at offset {msg.offset()}")
            else:
                raise KafkaException(msg.error())
        else:
            # Successfully received message
            try:
                # Decode the message (assuming base64 encoding)
                decoded_message = base64.b64decode(msg.value()).decode('utf-8')  # Decode bytes to string
                print(f"Received message: {decoded_message}")

                # Check if the message is empty
                if not decoded_message.strip():
                    print("Received an empty message, skipping...")
                    continue

                # Parse the decoded message as JSON
                try:
                    decoded_json = json.loads(decoded_message)  # Convert the JSON string into a dictionary
                    # Dump the JSON message
                    print(f"Dumped JSON: {json.dumps(decoded_json, indent=2)}")

                    # Insert the JSON into InfluxDB
                    point = Point("iot_data").tag("source", "kafka").field("data", json.dumps(decoded_json))
                    write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
                    print("Inserted JSON into InfluxDB")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e} - Message: {decoded_message}")
            except Exception as e:
                print(f"Error processing message: {e}")

except KeyboardInterrupt:
    print("Consumer interrupted, closing...")

finally:
    # Close the InfluxDB client
    influx_client.close()
    # Close the consumer gracefully
    consumer.close()
