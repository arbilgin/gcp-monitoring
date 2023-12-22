from google.cloud.monitoring_v3 import (Aggregation, ListTimeSeriesRequest,
                                        MetricServiceClient, TimeInterval)
from google.protobuf.timestamp_pb2 import Timestamp
from google.cloud import compute_v1


class GoogleMetrics:
    def __init__(
        self,
        client: MetricServiceClient,
        project: str,
        aggregation: Aggregation,
        interval: TimeInterval,
    ) -> None:
        self.client = client
        self.project = project
        self.aggregation = aggregation
        self.interval = interval
        self.data = {
            "cpu_utilization": [],
            "memory_utilization": [],
        }

    def get_cpu_utilization_for_vms(self) -> None:

        metric_type = "compute.googleapis.com/instance/cpu/utilization"
        query = f'resource.type="gce_instance" AND metric.type="{metric_type}"'

        results = self.client.list_time_series(
            request={
                "name": self.project,
                "filter": query,
                "interval": self.interval,
                "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": self.aggregation,
            }
        )
        for vm in results:
            self.data["cpu_utilization"].append(
                {
                    "machine": vm.metric.labels["instance_name"],
                    "utilization": round(vm.points[-1].value.double_value * 100, 2),
                }
            )
        return None


    def get_memory_utilization_for_vms(self) -> None:
        metric_type = "agent.googleapis.com/memory/percent_used"
        query =f'resource.type="gce_instance" AND metric.type="{metric_type}" AND metric.labels.state="used" '
        request = {
            "name": self.project,
            "filter": query,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": self.aggregation,
        }

        results = self.client.list_time_series(request=request)

        for result in results:
            self.data["memory_utilization"].append(
                {
                    "machine": result.resource.labels.get('instance_name', 'Unknown'),
                    "utilization": round(result.points[-1].value.double_value, 3),
                }
            )
        return None


    def get_data(self):
        self.get_cpu_utilization_for_vms()
        self.get_memory_utilization_for_vms()
        return self.data
