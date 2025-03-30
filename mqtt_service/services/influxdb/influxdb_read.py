from influxdb_client import InfluxDBClient, QueryApi

# Configuration for InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "mvmKmiT_b6hNSEvEYZKT2dhqnVsSq5mXoDsztOwrESzcOs6Fr5xpAO6hxZoeH4nW_0Ttvr46pAKkc4dppuSNAQ=="
influxdb_org = "ehs"
influxdb_bucket = "iot"

def read_influx_bucket(bucket_name, org, token, url, query):
    """
    Reads data from an InfluxDB bucket.

    :param bucket_name: Name of the bucket to read from.
    :param org: Organization name.
    :param token: Authentication token.
    :param url: InfluxDB URL.
    :param query: Flux query to execute.
    :return: Query results.
    """
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()
        result = query_api.query(query=query, org=org)
        return result


query = f'from(bucket: "{influxdb_bucket}") |> range(start: -1h)'
data = read_influx_bucket(influxdb_bucket, influxdb_org, influxdb_token, influxdb_url, query)
print(data)

# Print all data from the query results
for table in data:
    for record in table.records:
        print(f"Time: {record.get_time()}, Value: {record.get_value()}, Field: {record.get_field()}")
