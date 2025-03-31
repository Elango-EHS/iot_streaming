import time
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
from tabulate import tabulate  # Import tabulate for table formatting

# Configuration for InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "mvmKmiT_b6hNSEvEYZKT2dhqnVsSq5mXoDsztOwrESzcOs6Fr5xpAO6hxZoeH4nW_0Ttvr46pAKkc4dppuSNAQ=="
influxdb_org = "ehs"
influxdb_bucket = "iot"

# Initialize InfluxDB client
influx_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
query_api = influx_client.query_api()

# Continuously read new records
try:
    last_read_time = "-1m"  # Start by reading the last 1 minute of data
    while True:
        # Query to read data from InfluxDB
        query = f'''
        from(bucket: "{influxdb_bucket}")
        |> range(start: {last_read_time})
        |> filter(fn: (r) => r["_measurement"] == "iot_data")
        '''

        # Execute the query
        tables = query_api.query(query, org=influxdb_org)

        # Prepare data for tabular display
        table_data = []
        for table in tables:
            for record in table.records:
                table_data.append([record.get_time(), record.get_field(), record.get_value()])

        # Display the data in table format
        if table_data:
            print(tabulate(table_data, headers=["Time", "Field", "Value"], tablefmt="grid"))
        else:
            print("No new data found.")

        # Update the last read time to now
        last_read_time = "now()"

        # Wait for a short interval before querying again
        time.sleep(5)  # Adjust the interval as needed

except KeyboardInterrupt:
    print("Stopped reading from InfluxDB.")

except Exception as e:
    print(f"Error reading from InfluxDB: {e}")

finally:
    # Close the InfluxDB client
    influx_client.close()