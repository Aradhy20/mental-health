# Monitoring and Observability Setup for Mental Health App

## Overview
This guide provides instructions for setting up monitoring and observability for the Mental Health App using Prometheus, Grafana, and other tools.

## Prerequisites
- Docker and Docker Compose installed
- Mental Health App deployed using docker-compose.prod.yml

## 1. Prometheus Setup

Create a `prometheus.yml` configuration file:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'mental-health-services'
    static_configs:
      - targets: ['auth_service:8001', 'text_service:8002', 'voice_service:8003', 'face_service:8004', 'fusion_service:8005', 'doctor_service:8006', 'notification_service:8007', 'report_service:8008']
        labels:
          service: 'auth'
      - targets: ['text_service:8002']
        labels:
          service: 'text'
      - targets: ['voice_service:8003']
        labels:
          service: 'voice'
      - targets: ['face_service:8004']
        labels:
          service: 'face'
      - targets: ['fusion_service:8005']
        labels:
          service: 'fusion'
      - targets: ['doctor_service:8006']
        labels:
          service: 'doctor'
      - targets: ['notification_service:8007']
        labels:
          service: 'notification'
      - targets: ['report_service:8008']
        labels:
          service: 'report'

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

## 2. Grafana Setup

Create a `grafana/dashboards` directory and add dashboard JSON files for each service.

Sample dashboard configuration for text analysis service:

```json
{
  "dashboard": {
    "id": null,
    "title": "Text Analysis Service Metrics",
    "tags": ["text-analysis", "mental-health"],
    "timezone": "browser",
    "schemaVersion": 16,
    "version": 0,
    "refresh": "25s",
    "panels": [
      {
        "id": 1,
        "type": "graph",
        "title": "Request Duration",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])",
            "legendFormat": "{{handler}}"
          }
        ]
      },
      {
        "id": 2,
        "type": "singlestat",
        "title": "Total Requests",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "sum(http_requests_total)",
            "legendFormat": ""
          }
        ]
      }
    ]
  }
}
```

## 3. Updated Docker Compose with Monitoring

Update your `docker-compose.prod.yml` to include monitoring services:

```yaml
version: '3.8'

services:
  # Existing services...
  
  # Monitoring Services
  prometheus:
    image: prom/prometheus:latest
    container_name: mental_health_prometheus
    restart: always
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    networks:
      - app_network

  grafana:
    image: grafana/grafana-enterprise
    container_name: mental_health_grafana
    restart: always
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/var/lib/grafana/dashboards
      - ./grafana/grafana.ini:/etc/grafana/grafana.ini
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    networks:
      - app_network
    depends_on:
      - prometheus

  # Logging Services
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    container_name: mental_health_elasticsearch
    restart: always
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms1g -Xmx1g
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - app_network

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.0
    container_name: mental_health_kibana
    restart: always
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    networks:
      - app_network
    depends_on:
      - elasticsearch

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
  elasticsearch_data:

networks:
  app_network:
    driver: bridge
```

## 4. Instrumenting Services for Monitoring

Update your services to expose Prometheus metrics. Add the following to each service's main.py:

```python
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time

# Create metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status='2xx').inc()
    
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
    
    return response

# Add metrics endpoint
@app.get("/metrics")
async def metrics():
    from prometheus_client import generate_latest
    return Response(generate_latest())
```

## 5. Health Checks and Alerts

Configure health checks in your docker-compose file:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

Set up alerting rules in Prometheus:

```yaml
groups:
- name: mental-health-alerts
  rules:
  - alert: ServiceDown
    expr: up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Service {{ $labels.service }} is down"
      description: "{{ $labels.service }} has been down for more than 1 minute."

  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High error rate for {{ $labels.service }}"
      description: "Error rate for {{ $labels.service }} is above 5% for more than 2 minutes."
```

## 6. Running the Monitoring Stack

Start the complete stack with monitoring:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Access the monitoring tools:
- Grafana: http://localhost:3001 (admin/admin)
- Prometheus: http://localhost:9090
- Kibana: http://localhost:5601

## 7. Setting up Dashboards

1. Log into Grafana (http://localhost:3001)
2. Add Prometheus as a data source:
   - URL: http://prometheus:9090
3. Import the dashboard JSON files from the grafana/dashboards directory
4. Configure alerts in Grafana based on your requirements

## 8. Log Aggregation with ELK Stack

Configure Filebeat to ship logs to Elasticsearch:

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/mental-health/*.log
  json.keys_under_root: true
  json.add_error_key: true

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```

## 9. Best Practices

1. **Metric Naming**: Use consistent naming conventions
2. **Label Usage**: Don't overuse labels to avoid cardinality explosion
3. **Retention**: Set appropriate data retention periods
4. **Alerting**: Create actionable alerts with proper thresholds
5. **Dashboards**: Create meaningful dashboards for different user roles

## 10. Security Considerations

1. Change default passwords for Grafana and other tools
2. Restrict access to monitoring endpoints
3. Use HTTPS for all monitoring interfaces
4. Regularly update monitoring stack components
5. Implement proper authentication and authorization

This setup provides comprehensive monitoring and observability for your Mental Health App, enabling you to track performance, detect issues, and maintain system health.