# from google.cloud import compute_v1
from google.cloud.monitoring_v3 import (Aggregation, ListTimeSeriesRequest,
                                        MetricServiceClient, TimeInterval)
from google.protobuf.timestamp_pb2 import Timestamp


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
                    "utilization": round(vm.points[-1].value.double_value * 100, 3),
                }
            )
        return None

    def get_memory_utilization_for_vms(self) -> None:
        metric_type = "agent.googleapis.com/memory/percent_used"
        query = f'resource.type="gce_instance" AND metric.type="{metric_type}" AND metric.labels.state="used" '
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
                    "machine": result.resource.labels["instance_id"],
                    "utilization": round(result.points[-1].value.double_value, 3),
                }
            )
        return None

    def get_container_cpu_utilization_staging(self) -> None:
        metric_type = "kubernetes.io/container/cpu/limit_utilization"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="staging" '
        request = {
            "name": self.project,
            "filter": query,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": self.aggregation,
        }

        results = self.client.list_time_series(request=request)

        for result in results:
            self.data["cpu_utilization"].append(
                {
                    "machine": result.resource.labels["container_name"],
                    "utilization": round(result.points[-1].value.double_value, 3),
                    "env": result.resource.labels["namespace_name"],
                }
            )
        return None

    def get_container_cpu_utilization_prod(self) -> None:
        metric_type = "kubernetes.io/container/cpu/limit_utilization"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="prod" '
        request = {
            "name": self.project,
            "filter": query,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": self.aggregation,
        }

        results = self.client.list_time_series(request=request)

        for result in results:
            self.data["cpu_utilization"].append(
                {
                    "machine": result.resource.labels["container_name"],
                    "utilization": round(result.points[-1].value.double_value, 3),
                    "env": result.resource.labels["namespace_name"],
                }
            )
        return None

    def get_container_memory_utilization_staging(self) -> None:
        metric_type = "kubernetes.io/container/memory/limit_utilization"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="staging" AND metric.labels.memory_type="non-evictable" '
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
                    "machine": result.resource.labels["container_name"],
                    "utilization": round(result.points[-1].value.double_value, 3),
                    "env": result.resource.labels["namespace_name"],
                }
            )
        return None

    def get_container_memory_utilization_prod(self) -> None:
        metric_type = "kubernetes.io/container/memory/limit_utilization"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="prod" AND metric.labels.memory_type="non-evictable" '
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
                    "machine": result.resource.labels["container_name"],
                    "utilization": round(result.points[-1].value.double_value, 3),
                    "env": result.resource.labels["namespace_name"],
                }
            )
        return None

    # BUG: metric_type returns request cores 6 instead of limit cores 8
    def get_container_cpu_limit_staging(self) -> None:
        metric_type = "kubernetes.io/container/cpu/limit_cores"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="staging" '
        request = {
            "name": self.project,
            "filter": query,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
        }

        results = self.client.list_time_series(request=request)

        for result in results:
            self.data["cpu_utilization"].append(
                {
                    "cpu_limit": result.points[-1].value.double_value,
                    "env": result.resource.labels["namespace_name"],
                    "machine": result.resource.labels["container_name"],
                }
            )
        return None

    # BUG: metric_type returns request cores 6 instead of limit cores 8
    def get_container_cpu_limit_prod(self) -> None:
        metric_type = "kubernetes.io/container/cpu/limit_cores"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="prod" '
        request = {
            "name": self.project,
            "filter": query,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
        }

        results = self.client.list_time_series(request=request)

        for result in results:
            self.data["cpu_utilization"].append(
                {
                    "cpu_limit": result.points[-1].value.double_value,
                    "env": result.resource.labels["namespace_name"],
                    "machine": result.resource.labels["container_name"],
                }
            )
        return None

    # BUG: metric_type returns request bytes 12 Gi instead of limit bytes 16 Gi
    def get_container_memory_limit_staging(self) -> None:
        metric_type = "kubernetes.io/container/memory/limit_bytes"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="staging" '
        request = {
            "name": self.project,
            "filter": query,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
        }

        results = self.client.list_time_series(request=request)

        for result in results:
            self.data["memory_utilization"].append(
                {
                    "memory_limit": result.points[-1].value.int64_value / 1e+9, # Gi
                    "env": result.resource.labels["namespace_name"],
                    "machine": result.resource.labels["container_name"],
                }
            )
        return None

    # BUG: metric_type returns request bytes 12 Gi instead of limit bytes 16 Gi
    def get_container_memory_limit_prod(self) -> None:
        metric_type = "kubernetes.io/container/memory/limit_bytes"
        query = f'resource.type="k8s_container" AND metric.type="{metric_type}" AND resource.labels.cluster_name="greenlink-project-cluster" AND resource.labels.namespace_name="prod" '
        request = {
            "name": self.project,
            "filter": query,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
        }

        results = self.client.list_time_series(request=request)

        for result in results:
            self.data["memory_utilization"].append(
                {
                    "memory_limit": result.points[-1].value.int64_value / 1e+9, # Gi
                    "env": result.resource.labels["namespace_name"],
                    "machine": result.resource.labels["container_name"],
                }
            )
        return None

    def get_data(self):
        self.get_cpu_utilization_for_vms()
        self.get_memory_utilization_for_vms()
        self.get_container_cpu_utilization_staging()
        self.get_container_cpu_utilization_prod()
        self.get_container_memory_utilization_staging()
        self.get_container_memory_utilization_prod()
        self.get_container_cpu_limit_staging()
        self.get_container_cpu_limit_prod()
        self.get_container_memory_limit_staging()
        self.get_container_memory_limit_prod()
        return self.data
