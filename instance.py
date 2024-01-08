import time
from google.cloud import monitoring_v3

from google.cloud.monitoring_v3 import (Aggregation, ListTimeSeriesRequest,
                                        MetricServiceClient, TimeInterval)


def get_instance_name():
    client = monitoring_v3.MetricServiceClient()
    project_id = "greenlink-platform-396912"
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(time.time())},
            "start_time": {"seconds": int(time.time()) - 60 * 10},
        }
    )

    filter_str = f'resource.type="gce_instance" AND metric.type="compute.googleapis.com/instance/cpu/utilization"'
    results = client.list_time_series(
        name=f'projects/{project_id}',
        filter=filter_str,
        interval=interval,
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    
    for result in results:
        # instance_name = result.resource.labels['instance_name']
        # return result
        print(result)
    
if __name__ == "__main__":
    get_instance_name()