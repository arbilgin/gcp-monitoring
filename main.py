from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timedelta

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/greenlink-platform-396912"

aggregation = monitoring_v3.Aggregation(
   {
       "alignment_period": {"seconds": 60*10},  
       "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
   }
   )
def get_cpu_utilization(project_id, instance_id, time_interval_minutes):
    

    interval = monitoring_v3.TimeInterval()
    end_time = Timestamp()
    end_time.FromDatetime(datetime.utcnow())
    interval.end_time = end_time

    start_time = Timestamp()
    start_time.FromDatetime(datetime.utcnow() - timedelta(minutes=int(time_interval_minutes)))
    interval.start_time = start_time

    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    query = ( f'resource.type="gce_instance" AND resource.labels.instance_id="{instance_id}" '
               f'AND metric.type="{metric_type}" '
    )

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
        print(result)
        print(result.points[-1].interval.start_time, result.points[0].interval.end_time)
        for point in result.points:
            print(point.value.double_value*100)

def get_memory_utilization(project_id, instance_id, time_interval_minutes):

    interval = monitoring_v3.TimeInterval()
    end_time = Timestamp()
    end_time.FromDatetime(datetime.utcnow())
    interval.end_time = end_time

    start_time = Timestamp()
    start_time.FromDatetime(datetime.utcnow() - timedelta(minutes=int(time_interval_minutes)))
    interval.start_time = start_time

    metric_type = "agent.googleapis.com/memory/percent_used"
    query = ( f'resource.type="gce_instance" AND resource.labels.instance_id="{instance_id}" '
               f'AND metric.type="{metric_type}" AND metric.labels.state="used" '
    )
    request={
            "name": project_name,
            "filter": query,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
    }

    results = client.list_time_series(
        request=request
    )

    for result in results:
        print(result)
        print(result.points[-1].interval.start_time, result.points[0].interval.end_time)
        for point in result.points:
            print(point.value.double_value)


if __name__ == "__main__":
    project_id = "greenlink-platform-396912"
    instance_id = "4567250453145400611"
    time_interval_minutes = "10"
    get_cpu_utilization(project_id, instance_id, time_interval_minutes)
    get_memory_utilization(project_id, instance_id, time_interval_minutes)
