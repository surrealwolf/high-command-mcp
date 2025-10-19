# HTTP & Kubernetes Quick Start

## Quick Reference

### Run Locally with HTTP

```bash
# Install HTTP support
pip install high-command[http]

# Run server
MCP_TRANSPORT=http python -m highcommand.server

# In another terminal
curl http://localhost:8000/health
```

### Deploy to Kubernetes

```bash
# Install K8s support
pip install high-command[kubernetes]

# Build and push Docker image
docker build -t your-registry/high-command:latest .
docker push your-registry/high-command:latest

# Update image reference in k8s/deployment.yaml, then deploy
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Verify
kubectl get pods -l app=high-command
kubectl port-forward svc/high-command 8000:80
curl http://localhost:8000/health
```

## Environment Variables

```bash
# Transport mode
MCP_TRANSPORT=http           # http, sse, or stdio (default: stdio)

# Server configuration
MCP_HOST=0.0.0.0            # Listen address
MCP_PORT=8000               # Listen port
MCP_WORKERS=4               # Worker processes

# Logging
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR

# API client headers
X_SUPER_CLIENT=app          # Client identifier
X_SUPER_CONTACT=user@example.com  # Contact email
```

## API Endpoints

### Health Check
```bash
GET /health
Response: {"status": "healthy", "service": "high-command-mcp"}
```

### List Tools
```bash
POST /messages
Body: {"jsonrpc":"2.0","id":1,"method":"tools/list"}
```

### Call Tool
```bash
POST /messages
Body: {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_war_status",
    "arguments": {}
  }
}
```

### SSE Stream
```bash
GET /sse
# Server-Sent Events streaming
```

## Common Commands

```bash
# Local development
MCP_TRANSPORT=http MCP_PORT=8000 python -m highcommand.server

# High performance
MCP_TRANSPORT=http MCP_WORKERS=8 python -m highcommand.server

# Kubernetes deployment
kubectl apply -f k8s/

# Check deployment status
kubectl rollout status deployment/high-command

# View logs
kubectl logs -f deployment/high-command

# Port forward
kubectl port-forward svc/high-command 8000:80

# Test endpoint
curl http://localhost:8000/health
```

## Troubleshooting

### FastAPI/Uvicorn not installed
```bash
pip install high-command[http]
```

### Port already in use
```bash
MCP_PORT=9000 MCP_TRANSPORT=http python -m highcommand.server
```

### Kubernetes pod not running
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Health check failing
```bash
kubectl exec <pod-name> -- curl http://localhost:8000/health
```

## Configuration Files

### Docker
See `Dockerfile` in root directory

### Kubernetes
- `k8s/deployment.yaml` - Pod deployment
- `k8s/service.yaml` - Service definition
- `k8s/hpa.yaml` - Auto-scaling
- `k8s/rbac.yaml` - Permissions
- `k8s/network-policy.yaml` - Network rules

## Transport Modes

| Mode | Use Case | Performance |
|------|----------|-------------|
| stdio | VS Code, local | Native, no HTTP overhead |
| http | REST clients, Kubernetes | Good, standard web |
| sse | Browser, streaming | Good, real-time |

## Next Steps

1. Read [KUBERNETES_DEPLOYMENT.md](KUBERNETES_DEPLOYMENT.md) for detailed guide
2. See [docs/](docs/) for complete documentation
3. Check examples in [k8s/](k8s/) directory
4. Run `make help` for development commands

## Resources

- [Kubernetes Documentation](https://kubernetes.io/)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Project README](../README.md)
