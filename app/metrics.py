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

metrics_req_latency = Histogram('http_request_latency_seconds', 'HTTP Request Latency Seconds')
metrics_req_count = Counter('http_requests_total',
                            'Total HTTP Requests (count)',
                            ['method', 'endpoint', 'status_code'])
metrics_req_in_progress = Gauge("http_requests_inprogress",
                                "Number of in progress HTTP requests",
                                multiprocess_mode='livesum')
# metrics_req_time = Summary('request_processing_seconds', 'Time spent processing request')

