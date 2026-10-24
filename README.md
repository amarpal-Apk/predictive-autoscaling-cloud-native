# Intelligent Cloud-Native Autoscaling

This repository is organized for an intelligent cloud-native autoscaling project. The current implementation is the Java 17/Spring Boot order service; the ML prediction service, scaling controller, monitoring, and Kubernetes deployment directories are prepared for future work.

## Repository layout

- `services/order-service/` — Spring Boot REST API, PostgreSQL persistence, and tests.
- `infrastructure/docker/` — Docker Compose deployment for PostgreSQL and the order service.
- `infrastructure/monitoring/` — Prometheus and Grafana configuration.
- `infrastructure/kubernetes/` — Kubernetes manifests.
- `ml/` — datasets, training, and prediction service.
- `scaling-controller/` — autoscaling controller.
- `load-tests/k6/` — k6 load tests.
- `experiments/` — datasets and experiment results.
- `docs/` — architecture, research, diagrams, and progress documentation.
- `.github/` — workflow and issue-template configuration.

## Order service

See [`services/order-service/README.md`](services/order-service/README.md) for requirements, API endpoints, tests, and local/containerized run instructions.

Run the service and PostgreSQL from the repository root:

```powershell
docker compose -f infrastructure\docker\compose.yaml up --build -d
```
