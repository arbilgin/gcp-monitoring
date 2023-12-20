# from google.cloud import monitoring_v3

# import time

# client = monitoring_v3.MetricServiceClient()
# project = 'greenlink-platform-396912'  # TODO: Update to your project ID.
# project_name = f"projects/{project_id}"

# series = monitoring_v3.TimeSeries()
# series.metric.type = "custom.googleapis.com/my_metric"
# series.metric.labels["store_id"] = "Pittsburgh"
# series.resource.type = "gce_instance"
# series.resource.labels["instance_id"] = "1234567890123456789"
# series.resource.labels["zone"] = "us-central1-f"
# now = time.time()
# seconds = int(now)
# nanos = int((now - seconds) * 10**9)
# interval = monitoring_v3.TimeInterval(
#     {"end_time": {"seconds": seconds, "nanos": nanos}}
# )
# point = monitoring_v3.Point({"interval": interval, "value": {"double_value": 3.14}})
# series.points = [point]
# client.create_time_series(request={"name": project_name, "time_series": [series]})
# print("Successfully wrote time series.")
# return True

# from flask import Flask, render_template
# from google.cloud import monitoring_v3
# from google.auth.transport.requests import Request
# from google.auth import exceptions

# app = Flask(__name__)

# @app.route('/')
# def index():
#     cpu_data = get_cpu_utilization()
#     memory_data = get_memory_utilization()
#     return render_template('index.html', cpu_data=cpu_data, memory_data=memory_data)

# def get_cpu_utilization():
#     # Implement the logic to fetch CPU utilization from Google Cloud Monitoring API
#     # Replace this with your actual monitoring API calls
#     client = monitoring_v3.MetricServiceClient()
#     project = 'greenlink-platform-396912'  # TODO: Update to your project ID.
#     project_name = f"projects/{project_id}"
#     return "CPU Utilization Data"

# def get_memory_utilization():
#     # Implement the logic to fetch memory utilization from Google Cloud Monitoring API
#     # Replace this with your actual monitoring API calls
#     return "Memory Utilization Data"

# if __name__ == '__main__':
#     app.run(debug=True)

from google.cloud import monitoring_v3

import time

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/greenlink-platform-396912"
now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10**9)
interval = monitoring_v3.TimeInterval(
    {
        "end_time": {"seconds": seconds, "nanos": nanos},
        "start_time": {"seconds": (seconds - 240 ), "nanos": nanos},
    }
)
results = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization" ',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
)
for result in results:
    print(result)
#     for point in result.points:
#         print(point.value.double_value)


# resource_path = (
#     f"projects/greenlink-platform-396912/monitoredResourceDescriptors/gce_instance"
# )
# descriptor = client.get_monitored_resource_descriptor(name=resource_path)
# print(descriptor)
