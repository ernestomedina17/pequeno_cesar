from prometheus_client import Summary, Histogram, Gauge, Counter

# METRICS - https://github.com/prometheus/client_python
# Limitations:
# Registries can not be used as normal, all instantiated metrics are exported
# Custom collectors do not work (e.g. cpu and memory metrics)
# Info and Enum metrics do not work
# The pushgateway cannot be used
# Gauges cannot use the pid label.
#
# When Gauge metrics are used, additional tuning needs to be performed. Gauges have several modes
# they can run in, which can be selected with the multiprocess_mode parameter:
#  'all': Default. Return a timeseries per process alive or dead.
#  'liveall': Return a timeseries per process that is still alive.
#  'livesum': Return a single timeseries that is the sum of the values of alive processes.
#  'max': Return a single timeseries that is the maximum of the values of all processes, alive or dead.
#  'min': Return a single timeseries that is the minimum of the values of all processes, alive or dead.

metrics_req_latency = Histogram(__name__.replace('.', '_') + '_request_latency_seconds',
                                'Flask Request Latency')
# metrics_req_time = Summary('request_processing_seconds', 'Time spent processing request')
# metrics_req_count = Counter('my_failures', 'Description of counter')
# metrics_req_in_progress = Gauge("inprogress_requests", "help", multiprocess_mode='livesum')
# metrics_req_label = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
# @metrics_req_label.labels('get', '/').inc()
# @metrics_req_label.labels('post', '/submit').inc()
