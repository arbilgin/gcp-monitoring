import time
from datetime import datetime, timedelta

from flask import Flask, render_template
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp

# app = Flask(__name__)

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/greenlink-platform-396912"

aggregation = monitoring_v3.Aggregation(
    {
        "alignment_period": {"seconds": 60 * 10},
        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    }
)

# project_id = "greenlink-platform-396912"
# instance_id = "4567250453145400611"
time_interval_minutes = "10"
# container_name = "task-queue"
# namespace_name = "staging"

# @app.route('/')
# def index():
#     cpu_data = get_cpu_utilization()
#     memory_data = get_memory_utilization()
#     return render_template('index.html', cpu_data=cpu_data, memory_data=memory_data)


def get_cpu_utilization():
    interval = monitoring_v3.TimeInterval()
    end_time = Timestamp()
    end_time.FromDatetime(datetime.utcnow())
    interval.end_time = end_time

    start_time = Timestamp()
    start_time.FromDatetime(
        datetime.utcnow() - timedelta(minutes=int(time_interval_minutes))
    )
    interval.start_time = start_time

    # now = time.time()
    # seconds = int(now)
    # nanos = int((now - seconds) * 10**9)
    # interval = monitoring_v3.TimeInterval(
    #     {
    #         "end_time": {"seconds": seconds, "nanos": nanos},
    #         "start_time": {"seconds": (seconds - 600 ), "nanos": nanos},
    #     }
    # )

    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    query = f'resource.type="gce_instance" ' f'AND metric.type="{metric_type}" '

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": query,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(
            result.metric.labels["instance_name"],
            "{}%".format(round(result.points[-1].value.double_value * 100, 2)),
        )
        # return result.metric.labels["instance_name"], "{}%".format(round(result.points[-1].value.double_value*100, 2))
        # print(result.points[-1].interval.start_time, result.points[0].interval.end_time)
        # for point in result.points:
        #     print(point.value.double_value*100)


def get_memory_utilization():
    interval = monitoring_v3.TimeInterval()
    end_time = Timestamp()
    end_time.FromDatetime(datetime.utcnow())
    interval.end_time = end_time

    start_time = Timestamp()
    start_time.FromDatetime(
        datetime.utcnow() - timedelta(minutes=int(time_interval_minutes))
    )
    interval.start_time = start_time

    metric_type = "agent.googleapis.com/memory/percent_used"
    query = (
        f'resource.type="gce_instance" '
        f'AND metric.type="{metric_type}" AND metric.labels.state="used" '
    )
    request = {
        "name": project_name,
        "filter": query,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }

    results = client.list_time_series(request=request)

    for result in results:
        # print(result)
        print(
            result.resource.labels["instance_id"],
            "{}%".format(round(result.points[-1].value.double_value, 3)),
        )
        # print(result.points[-1].interval.start_time, result.points[0].interval.end_time)
        # for point in result.points:
        #     print(point.value.double_value)
        #     return "{} %".format(point.value.double_value)


def get_container_cpu_utilization_staging():
    time_interval_minutes = "10"
    # container_name = "task-queue"
    namespace_name = "staging"

    interval = monitoring_v3.TimeInterval()
    end_time = Timestamp()
    end_time.FromDatetime(datetime.utcnow())
    interval.end_time = end_time

    start_time = Timestamp()
    start_time.FromDatetime(
        datetime.utcnow() - timedelta(minutes=int(time_interval_minutes))
    )
    interval.start_time = start_time

    metric_type = "kubernetes.io/container/cpu/limit_utilization"
    query = (
        f'resource.type="k8s_container" '
        f'AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="{namespace_name}"  '
        f'AND metric.type="{metric_type}" '
    )
    request = {
        "name": project_name,
        "filter": query,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }

    results = client.list_time_series(request=request)

    for result in results:
        print(
            result.resource.labels["namespace_name"],
            result.resource.labels["container_name"],
            "{}%".format(round(result.points[-1].value.double_value * 100, 2)),
        )
        # print(result)
        # print(result.points[-1].interval.start_time, result.points[0].interval.end_time)
        # for point in result.points:
        #     print(point.value.double_value * 100)


def get_container_cpu_utilization_prod():
    time_interval_minutes = "10"
    # container_name = "task-queue"
    namespace_name = "prod"

    interval = monitoring_v3.TimeInterval()
    end_time = Timestamp()
    end_time.FromDatetime(datetime.utcnow())
    interval.end_time = end_time

    start_time = Timestamp()
    start_time.FromDatetime(
        datetime.utcnow() - timedelta(minutes=int(time_interval_minutes))
    )
    interval.start_time = start_time

    metric_type = "kubernetes.io/container/cpu/limit_utilization"
    query = (
        f'resource.type="k8s_container" '
        f'AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="{namespace_name}"  '
        f'AND metric.type="{metric_type}" '
    )
    request = {
        "name": project_name,
        "filter": query,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }

    results = client.list_time_series(request=request)

    for result in results:
        print(
            result.resource.labels["namespace_name"],
            result.resource.labels["container_name"],
            "{}%".format(round(result.points[-1].value.double_value * 100, 2)),
        )


def get_container_memory_utilization_staging():
    time_interval_minutes = "10"
    # container_name = "task-queue"
    namespace_name = "staging"

    interval = monitoring_v3.TimeInterval()
    end_time = Timestamp()
    end_time.FromDatetime(datetime.utcnow())
    interval.end_time = end_time

    start_time = Timestamp()
    start_time.FromDatetime(
        datetime.utcnow() - timedelta(minutes=int(time_interval_minutes))
    )
    interval.start_time = start_time

    metric_type = "kubernetes.io/container/memory/limit_utilization"
    query = (
        f'resource.type="k8s_container" '
        f'AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="{namespace_name}" '
        f'AND metric.type="{metric_type}" AND metric.labels.memory_type="non-evictable"'
    )
    request = {
        "name": project_name,
        "filter": query,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }

    results = client.list_time_series(request=request)

    for result in results:
        # print(result)
        print(
            result.resource.labels["namespace_name"],
            result.resource.labels["container_name"],
            "{}%".format(round(result.points[-1].value.double_value * 100, 2)),
        )


def get_container_memory_utilization_prod():
    time_interval_minutes = "10"
    namespace_name = "prod"

    interval = monitoring_v3.TimeInterval()
    end_time = Timestamp()
    end_time.FromDatetime(datetime.utcnow())
    interval.end_time = end_time

    start_time = Timestamp()
    start_time.FromDatetime(
        datetime.utcnow() - timedelta(minutes=int(time_interval_minutes))
    )
    interval.start_time = start_time

    metric_type = "kubernetes.io/container/memory/limit_utilization"
    query = (
        f'resource.type="k8s_container" '
        f'AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="{namespace_name}" '
        f'AND metric.type="{metric_type}" AND metric.labels.memory_type="non-evictable" '
    )
    request = {
        "name": project_name,
        "filter": query,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }

    results = client.list_time_series(request=request)

    for result in results:
        # print(result)
        print(
            result.resource.labels["namespace_name"],
            result.resource.labels["container_name"],
            "{}%".format(round(result.points[-1].value.double_value * 100, 2)),
        )

def get_container_cpu_limit_staging():
        interval = monitoring_v3.TimeInterval()
        end_time = Timestamp()
        end_time.FromDatetime(datetime.utcnow())
        interval.end_time = end_time

        start_time = Timestamp()
        start_time.FromDatetime(
            datetime.utcnow() - timedelta(minutes=int(time_interval_minutes))
        )
        interval.start_time = start_time
        metric_type = "kubernetes.io/container/cpu/limit_cores"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="staging" '
        request = {
            "name": project_name,
            "filter": query,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }

        results = client.list_time_series(request=request)

        for result in results:
            print(result)

if __name__ == "__main__":
    get_cpu_utilization()
    get_memory_utilization()
    get_container_cpu_utilization_staging()
    get_container_cpu_utilization_prod()
    get_container_memory_utilization_staging()
    get_container_memory_utilization_prod()
    get_container_cpu_limit_staging()
#  app.run(debug=True)
