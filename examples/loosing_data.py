import time
from datetime import datetime
from influxdb_client import InfluxDBClient, WriteOptions, Point

token = "..."
org = "..."
bucket = "..."
measurement = "Pressure"

client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token, debug=True)
write_api = client.write_api(
    write_options=WriteOptions(batch_size=8, flush_interval=8, jitter_interval=0, retry_interval=1000))
for i in range(50):
    valOne = float(i)
    valTwo = float(i) + 0.5
    pointOne = Point(measurement).tag("sensor", "sensor1").field("PSI", valOne).time(time=datetime.utcnow())
    pointTwo = Point(measurement).tag("sensor", "sensor2").field("PSI", valTwo).time(time=datetime.utcnow())

    write_api.write(bucket, org, [pointOne, pointTwo])
    print("PSI Readings: (%f, %f)" % (valOne, valTwo))
    time.sleep(0.5)

write_api.__del__()

query = f'from(bucket: "{bucket}") |> range(start: 0) |> filter(fn: (r) => r["_measurement"] == "{measurement}") |> count()'
tables = client.query_api().query(query, org)
for table in tables:
    for record in table.records:
        print(f'{record.get_measurement()}: {record.get_field()} count: {record.get_value()}')

client.__del__()
print("end")


