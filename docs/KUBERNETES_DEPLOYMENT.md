# Kubernetes Deployment Guide

This guide shows how to deploy the High-Command MCP Server on Kubernetes with HTTP/SSE support.

## Overview

The High-Command server now supports HTTP transport via FastAPI and uvicorn, making it Kubernetes-ready with:

- ✅ **Health checks** - Liveness and readiness probes
- ✅ **Horizontal scaling** - Run multiple replicas
- ✅ **Load balancing** - Distribute requests across pods
- ✅ **Service discovery** - Kubernetes DNS integration
- ✅ **Resource management** - CPU/memory limits and requests

## Prerequisites

- Kubernetes 1.20+
- kubectl CLI configured
- Docker registry access
- Python 3.14+ (for building images)

## Installation

### 1. Install with HTTP Support

```bash
pip install high-command[http]
```

### 2. Build Docker Image

```bash
# Build for HTTP transport
make docker-build

# Or manually
docker build -t high-command:latest .
```

### 3. Push to Registry

```bash
docker tag high-command:latest your-registry/high-command:latest
docker push your-registry/high-command:latest
```

## Kubernetes Deployment

### Basic Deployment

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: high-command
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: high-command
  template:
    metadata:
      labels:
        app: high-command
    spec:
      containers:
      - name: high-command
        image: your-registry/high-command:latest
        imagePullPolicy: IfNotPresent
        
        # HTTP Transport Configuration
        env:
        - name: MCP_TRANSPORT
          value: "http"
        - name: MCP_HOST
          value: "0.0.0.0"
        - name: MCP_PORT
          value: "8000"
        - name: MCP_WORKERS
          value: "4"
        - name: LOG_LEVEL
          value: "INFO"
        
        # Optional: HellHub API Configuration
        - name: X_SUPER_CLIENT
          value: "hc.k8s.cluster"
        - name: X_SUPER_CONTACT
          value: "ops@example.com"
        
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        
        # Health Checks
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 30
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 2
        
        # Resource Management
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        
        # Security Context
        securityContext:
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
```

### Service Configuration

Create `k8s/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: high-command
  namespace: default
spec:
  type: ClusterIP
  selector:
    app: high-command
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  sessionAffinity: None
```

### Horizontal Pod Autoscaler

Create `k8s/hpa.yaml`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: high-command-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: high-command
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### ConfigMap for Configuration

Create `k8s/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: high-command-config
  namespace: default
data:
  LOG_LEVEL: "INFO"
  MCP_WORKERS: "4"
  X_SUPER_CLIENT: "hc.k8s.cluster"
```

## Deployment

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace high-command

# Apply configurations
kubectl apply -f k8s/configmap.yaml -n high-command
kubectl apply -f k8s/deployment.yaml -n high-command
kubectl apply -f k8s/service.yaml -n high-command
kubectl apply -f k8s/hpa.yaml -n high-command

# Verify deployment
kubectl get pods -n high-command
kubectl get svc -n high-command
```

### Check Status

```bash
# Watch rollout
kubectl rollout status deployment/high-command -n high-command

# View logs
kubectl logs -f deployment/high-command -n high-command

# Describe deployment
kubectl describe deployment high-command -n high-command
```

## Usage

### Direct HTTP Calls

```bash
# Port forward to local machine
kubectl port-forward svc/high-command 8000:80 -n high-command

# Get health status
curl http://localhost:8000/health

# Get war status
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "get_war_status",
      "arguments": {}
    }
  }'
```

### SSE Connection

```bash
# Connect to SSE endpoint for streaming updates
curl http://localhost:8000/sse
```

### From VS Code

Update `~/.config/Code/User/mcp.json`:

```json
{
  "servers": {
    "high-command": {
      "type": "http",
      "url": "http://high-command.default.svc.cluster.local/sse"
    }
  }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_TRANSPORT` | `stdio` | Transport type: `stdio`, `http`, or `sse` |
| `MCP_HOST` | `0.0.0.0` | Listen address |
| `MCP_PORT` | `8000` | Listen port |
| `MCP_WORKERS` | `4` | Number of worker processes |
| `LOG_LEVEL` | `INFO` | Logging level |
| `X_SUPER_CLIENT` | `hc.dataknife.ai` | Client identifier |
| `X_SUPER_CONTACT` | `lee@fullmetal.dev` | Contact email |

## Monitoring

### Prometheus Metrics

High-Command automatically exposes Prometheus metrics at `/metrics` (when available):

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: high-command
spec:
  selector:
    matchLabels:
      app: high-command
  endpoints:
  - port: http
    interval: 30s
    path: /metrics
```

### Logging

View centralized logs with:

```bash
kubectl logs -f deployment/high-command -n high-command --all-containers
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n high-command

# View logs
kubectl logs <pod-name> -n high-command
```

### Health Check Failures

```bash
# Test health endpoint directly
kubectl exec <pod-name> -n high-command -- \
  curl -s http://localhost:8000/health
```

### High Memory Usage

Reduce `MCP_WORKERS` or increase memory limits:

```yaml
env:
- name: MCP_WORKERS
  value: "2"

resources:
  limits:
    memory: "1Gi"
```

## Performance Tuning

### Worker Threads

Adjust workers based on CPU cores:
- 2 cores: 2-4 workers
- 4 cores: 4-8 workers
- 8+ cores: 8-16 workers

```yaml
env:
- name: MCP_WORKERS
  value: "8"
```

### Connection Pooling

Configure httpx connection pool limits in the API client:

```python
# In highcommand/api_client.py
limits = httpx.Limits(
    max_connections=100,
    max_keepalive_connections=20,
)
```

## Security Best Practices

1. **Network Policies** - Restrict traffic to/from pods
2. **RBAC** - Use role-based access control
3. **TLS/HTTPS** - Terminate SSL at ingress
4. **Secrets** - Use Kubernetes secrets for sensitive data
5. **Resource Limits** - Always set CPU and memory limits

### Example Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: high-command-netpol
spec:
  podSelector:
    matchLabels:
      app: high-command
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: default
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # For HTTPS to HellHub API
```

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Server](https://www.uvicorn.org/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [HellHub API](https://hellhub-collective.gitbook.io/)
