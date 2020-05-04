from prometheus_client import Summary, Histogram, Gauge, Counter

# 4 types of Metrics:
# - Counter: goes up only, like website visits.
# - Gauge:  goes up or down, cpu or temperature.
# - Histogram: observations, request duration(latency), response sizes. Observations get counted into buckets.
#   Includes (_count and _sum). Main purpose is calculating quantiles.
# - Summary: observations, request duration, response sizes. ALso includes TOTAL sum of observed values,
#   it calculates quantiles over a sliding time window.
#
# Two rules of thumb:
# If you need to aggregate, choose histograms.
# Otherwise, choose a histogram if you have an idea of the range and distribution of values that will be observed.
# Choose a summary if you need an accurate quantile, no matter what the range and distribution of the values is.

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

metrics_req_latency = Histogram('pequeno_cesar_flask_request_latency_seconds',
                                'HTTP Request Latency Seconds')

metrics_req_count = Counter('pequeno_cesar_flask_requests_total',
                            'Total HTTP Requests Count',
                            ['method', 'endpoint', 'status_code'])

metrics_req_in_progress = Gauge("pequeno_cesar_flask_requests_inprogress",
                                "Number of in progress HTTP requests",
                                multiprocess_mode='livesum')

metrics_query_latency = Histogram('pequeno_cesar_neo4j_request_latency_seconds',
                                  'Neo4j Bolt Cypher Query Latency Seconds')

metrics_query_count = Counter('pequeno_cesar_neo4j_requests_total',
                              'Total Neo4j Bolt Cypher Query Count',
                              ['object', 'method'])

metrics_query_in_progress = Gauge("pequeno_cesar_neo4j_requests_inprogress",
                                  "Number of in progress Neo4j Bolt Cypher Queries",
                                  multiprocess_mode='livesum')
