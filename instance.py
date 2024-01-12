import time
from google.cloud import monitoring_v3

from google.cloud.monitoring_v3 import (Aggregation, ListTimeSeriesRequest,
                                        MetricServiceClient, TimeInterval)


def get_node_memory_utilization():
    client = monitoring_v3.MetricServiceClient()
    project = f"projects/greenlink-platform-396912"
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(time.time())},
            "start_time": {"seconds": int(time.time()) - 60 * 10},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 60 * 10},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        }
    )
    metric_type = "kubernetes.io/node/memory/total_bytes"
    query = f'resource.type="k8s_node" AND metric.type="{metric_type}" '
    request = {
        "name": project,
        "filter": query,
        "interval": interval,
        "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": aggregation,
    }
    results = client.list_time_series(request=request)
    
    for result in results:
        # instance_name = result.resource.labels['instance_name']
        # return result
        print(result)
    
if __name__ == "__main__":
    get_node_memory_utilization()