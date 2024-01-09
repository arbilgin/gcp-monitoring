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
        self.data = {}

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
            machine_name = vm.metric.labels["instance_name"]
            cpu_utilization = "{} %".format(round(vm.points[-1].value.double_value * 100, 3))
            if machine_name in self.data:
                self.data[machine_name]["cpu_utilization"] = cpu_utilization
                self.data[machine_name]["env"] = "VM/Cluster node"
            else:
                self.data[machine_name] = {"cpu_utilization": cpu_utilization}
                self.data[machine_name]["env"] = "VM/Cluster node" 
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
            metric_type = "compute.googleapis.com/instance/cpu/utilization"
            instance_id = result.resource.labels["instance_id"]
            filter = f'metric.type="{metric_type}" AND resource.labels.instance_id="{instance_id}"'
            outcomes = self.client.list_time_series(
                name=self.project,
                filter=filter,
                interval=self.interval,
                view=ListTimeSeriesRequest.TimeSeriesView.FULL,
            )
            for outcome in outcomes:
                machine_name = outcome.metric.labels["instance_name"]
            
            memory_utilization = "{} %".format(round(result.points[-1].value.double_value, 3))
            if machine_name in self.data:
                self.data[machine_name]["memory_utilization"] = memory_utilization
                self.data[machine_name]["env"] = "VM/Cluster node"
            else:
                self.data[machine_name] = {"memory_utilization": memory_utilization}
                self.data[machine_name]["env"] = "VM/Cluster node" 

            # machine_name = result.resource.labels["instance_id"]
            # memory_utilization = round(result.points[-1].value.double_value, 3)
            # if machine_name in self.data:
            #     self.data[machine_name]["memory_utilization"] = memory_utilization
            #     self.data[machine_name]["env"] = "VM/Cluster node"
            # else:
            #     self.data[machine_name] = {"memory_utilization": memory_utilization}
            #     self.data[machine_name]["env"] = "VM/Cluster node" 
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
            machine_name = result.resource.labels["container_name"]
            cpu_utilization = "{} %".format(round(result.points[-1].value.double_value, 3))
            env = result.resource.labels["namespace_name"]
            if machine_name in self.data:
                self.data[machine_name]["cpu_utilization"] = cpu_utilization
                self.data[machine_name]["env"] = env
            else:
                self.data[machine_name] = {"cpu_utilization": cpu_utilization}
                self.data[machine_name]["env"] = env
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
            machine_name = result.resource.labels["container_name"]
            cpu_utilization = "{} %".format(round(result.points[-1].value.double_value, 3))
            env = result.resource.labels["namespace_name"]
            if machine_name in self.data:
                self.data[machine_name]["cpu_utilization"] = cpu_utilization
                self.data[machine_name]["env"] = env
            else:
                self.data[machine_name] = {"cpu_utilization": cpu_utilization}
                self.data[machine_name]["env"] = env
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
            machine_name = result.resource.labels["container_name"]
            memory_utilization = "{} %".format(round(result.points[-1].value.double_value, 3))
            env = result.resource.labels["namespace_name"]
            if machine_name in self.data:
                self.data[machine_name]["memory_utilization"] = memory_utilization
                self.data[machine_name]["env"] = env
            else:
                self.data[machine_name] = {"memory_utilization": memory_utilization}
                self.data[machine_name]["env"] = env
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
            machine_name = result.resource.labels["container_name"]
            memory_utilization = "{} %".format(round(result.points[-1].value.double_value, 3))
            env = result.resource.labels["namespace_name"]
            if machine_name in self.data:
                self.data[machine_name]["memory_utilization"] = memory_utilization
                self.data[machine_name]["env"] = env
            else:
                self.data[machine_name] = {"memory_utilization": memory_utilization}
                self.data[machine_name]["env"] = env
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
            machine_name = result.resource.labels["container_name"]
            env = result.resource.labels["namespace_name"]
            cpu_limit = "{} cores".format(result.points[-1].value.double_value)
            if machine_name in self.data:
                self.data[machine_name]["cpu_limit"] = cpu_limit
                self.data[machine_name]["env"] = env
            else:
                self.data[machine_name] = {"cpu_limit": cpu_limit}
                self.data[machine_name]["env"] = env
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
            machine_name = result.resource.labels["container_name"]
            env = result.resource.labels["namespace_name"]
            cpu_limit = "{} cores".format(result.points[-1].value.double_value)
            if machine_name in self.data:
                self.data[machine_name]["cpu_limit"] = cpu_limit
                self.data[machine_name]["env"] = env
            else:
                self.data[machine_name] = {"cpu_limit": cpu_limit}
                self.data[machine_name]["env"] = env
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
            machine_name = result.resource.labels["container_name"]
            env = result.resource.labels["namespace_name"]
            memory_limit = "{} Gi".format(result.points[-1].value.int64_value / 1e+9) # Gi
            if machine_name in self.data:
                self.data[machine_name]["memory_limit"] = memory_limit
                self.data[machine_name]["env"] = env
            else:
                self.data[machine_name] = {"memory_limit": memory_limit}
                self.data[machine_name]["env"] = env
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
            machine_name = result.resource.labels["container_name"]
            env = result.resource.labels["namespace_name"]
            memory_limit = "{} Gi".format(result.points[-1].value.int64_value / 1e+9) # Gi
            if machine_name in self.data:
                self.data[machine_name]["memory_limit"] = memory_limit
                self.data[machine_name]["env"] = env
            else:
                self.data[machine_name] = {"memory_limit": memory_limit}
                self.data[machine_name]["env"] = env
        return None


    def get_node_memory_utilization(self) -> None:
        
        # 1 - GET TOTAL BYTES
        metric_type_total = "kubernetes.io/node/memory/total_bytes"
        query_total = f'resource.type="k8s_node" AND metric.type="{metric_type_total}" '
        request_total = {
            "name": self.project,
            "filter": query_total,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": self.aggregation,
        }

        total_bytes_results = self.client.list_time_series(request=request_total)

        # 2 - GET USED BYTES
        metric_type = "kubernetes.io/node/memory/used_bytes"
        query = f'resource.type="k8s_node" AND metric.type="{metric_type}" AND metric.labels.memory_type="non-evictable"'
        request = {
            "name": self.project,
            "filter": query,
            "interval": self.interval,
            "view": ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": self.aggregation,
        }

        used_bytes_results = list(self.client.list_time_series(request=request)) # 6 nodes
        
        # Calculate total and used bytes
        n = 0
        for each in total_bytes_results:
            machine_name = each.resource.labels["node_name"]
            memory_total = each.points[-1].value.double_value / 1e+9 # Gi
            memory_used = used_bytes_results[n].points[-1].value.double_value / 1e+9 # Gi
            memory_utilization = memory_used / memory_total * 100
            if machine_name in self.data:
                self.data[machine_name]["memory_utilization"] = f"{round(memory_utilization, 2)}%"
            else:
                self.data[machine_name] = {"memory_utilization": f"{round(memory_utilization, 2)}%"}
            n += 1

        return None

        # for result in results:
        #     machine_name = result.resource.labels["node_name"]
        #     memory_utilization = result.points[-1].value.double_value / 1e+9
        #     if machine_name in self.data:
        #         self.data[machine_name]["memory_utilization"] = memory_utilization
        #     else:
        #         self.data[machine_name] = {"memory_utilization": memory_utilization}
        # return None
    def get_data(self):
        self.get_cpu_utilization_for_vms()
        self.get_memory_utilization_for_vms()
        self.get_container_cpu_utilization_staging()
        self.get_container_cpu_utilization_prod()
        self.get_container_memory_utilization_staging()
        self.get_container_memory_utilization_prod()
        self.get_container_cpu_limit_prod()
        self.get_container_cpu_limit_staging()
        self.get_container_memory_limit_staging()
        self.get_container_memory_limit_prod()
        # self.get_node_memory_utilization()
        return self.data
