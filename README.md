# Intelligent Cloud-Native Autoscaling

This repository is organized for an intelligent cloud-native autoscaling project. The current implementation is the Java 17/Spring Boot order service. The API gateway, catalog service, ML components, monitoring, and Kubernetes deployment directories are prepared for future work.

## Repository layout

- `services/order-service/` — Spring Boot REST API, PostgreSQL persistence, and tests.
- `services/api-gateway/` — API gateway service.
- `services/catalog-service/` — product catalog service.
- `infrastructure/docker/` — Docker Compose deployment for PostgreSQL and the order service.
- `infrastructure/monitoring/` — monitoring configuration.
- `infrastructure/kubernetes/` — Kubernetes manifests.
- `ml/training/` — model training code.
- `ml/prediction-service/` — model inference service.
- `ml/scaling-controller/` — autoscaling controller.
- `load-tests/k6/` — k6 load tests.
- `experiments/` — datasets and experiment results.
- `docs/` — architecture, research, and progress documentation.
- `.github/` — workflow and issue-template configuration.

## Order service

See [`services/order-service/README.md`](services/order-service/README.md) for requirements, API endpoints, tests, and local/containerized run instructions.

Run the service and PostgreSQL from the repository root:

```powershell
docker compose -f infrastructure\docker\compose.yaml up --build -d
```

## Load test

Install [k6](https://grafana.com/docs/k6/latest/set-up/install-k6/), start the order service, then run from the repository root:

```powershell
k6 run load-tests\k6\load-test.js
```

The test creates, retrieves, and lists orders against `http://localhost:8080`. To target another service URL, set `BASE_URL`:

```powershell
$env:BASE_URL = "http://localhost:8080"
k6 run load-tests\k6\load-test.js
```
