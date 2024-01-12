import time

from flask import Flask, render_template
from google.cloud import monitoring_v3

from metrics import GoogleMetrics

app = Flask(__name__)


def setup_metrics():
    client = monitoring_v3.MetricServiceClient()
    project = f"projects/greenlink-platform-396912"
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 60 * 10},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        }
    )
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(time.time())},
            "start_time": {"seconds": int(time.time()) - 60 * 10},
        }
    )
    metrics = GoogleMetrics(client, project, aggregation, interval)
    return metrics


metrics = setup_metrics()
data = metrics.get_data()
from pprint import pprint

pprint(data)
