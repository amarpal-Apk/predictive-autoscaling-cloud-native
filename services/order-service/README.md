# M.Tech Order Service

A small Java 17 and Spring Boot REST API backed by PostgreSQL. The first increment is intentionally a single service that runs locally or with Docker Compose.

## Requirements

- Java 17
- Maven 3.9+
- Docker Desktop with Docker Compose v2 (for the containerized run)

## Build and test

From the repository root, run:

```powershell
Set-Location services\order-service
mvn clean test
mvn clean package
```

The tests use mocked repositories and the Spring MVC test framework, so they do not require Docker or a running PostgreSQL server.

## Run locally

From the repository root, start PostgreSQL in Docker:

```powershell
docker compose -f infrastructure\docker\compose.yaml up -d postgres
```

Start the API in another PowerShell window, from `services\order-service`:

```powershell
mvn spring-boot:run
```

Stop the API with `Ctrl+C`, then stop PostgreSQL from the repository root:

```powershell
docker compose -f infrastructure\docker\compose.yaml down
```

## Run the API and PostgreSQL in Docker

From the repository root:

```powershell
docker compose -f infrastructure\docker\compose.yaml up --build -d
docker compose -f infrastructure\docker\compose.yaml ps
docker compose -f infrastructure\docker\compose.yaml logs -f order-service
```

Stop the containers while preserving the local database volume:

```powershell
docker compose -f infrastructure\docker\compose.yaml down
```

To also remove the local database data, run `docker compose down -v`. This deletes the PostgreSQL data volume.

The Compose configuration limits the API container to 512 MB and PostgreSQL to 256 MB. PostgreSQL is tuned with a 64 MB shared buffer and 30 maximum connections; the JVM adjusts its heap based on the container memory limit. The local credentials in `infrastructure/docker/compose.yaml` are for development only.

## API

The API listens on `http://localhost:8080`.

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/orders` | Create an order |
| `GET` | `/api/orders/{id}` | Get an order by ID |
| `GET` | `/api/orders` | List orders |
| `GET` | `/api/test` | Basic service test endpoint |
| `GET` | `/actuator/health` | Health status |
| `GET` | `/actuator/info` | Application information |
| `GET` | `/actuator/metrics` | Available application metrics |
| `GET` | `/actuator/prometheus` | Prometheus metrics |

Create an order from PowerShell:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://localhost:8080/api/orders `
  -ContentType "application/json" `
  -Body '{"customerName":"Ava","productName":"Keyboard","quantity":2}'
```

Fetch all orders:

```powershell
Invoke-RestMethod -Uri http://localhost:8080/api/orders
```

Check health and metrics:

```powershell
Invoke-RestMethod -Uri http://localhost:8080/actuator/health
Invoke-RestMethod -Uri http://localhost:8080/actuator/info
Invoke-RestMethod -Uri http://localhost:8080/actuator/metrics
Invoke-WebRequest -Uri http://localhost:8080/actuator/prometheus
```

Order creation requires a non-blank customer name (up to 100 characters), a non-blank product name (up to 150 characters), and a positive quantity. Invalid requests return HTTP 400; unknown order IDs return HTTP 404. Error responses include a timestamp, status, message, and field validation errors when applicable.

## Configuration

The default database settings are for local PostgreSQL. Override them with `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, and `DB_PASSWORD`. The JPA schema is updated automatically for this development project; use a migration tool before deploying to a production environment.

## Initial architecture decisions

- Spring Boot 3.5.x supports Java 17 and provides the API, validation, persistence, and Actuator integration.
- A request/response DTO boundary prevents the persistence entity from becoming the public API contract.
- PostgreSQL is the runtime database; tests mock the repository to keep `mvn test` fast and independent of Docker.
- Docker Compose contains only the API and PostgreSQL. Health-based startup ordering avoids connecting the API before PostgreSQL is ready.
- Prometheus metrics are provided through Actuator and Micrometer without introducing a separate monitoring stack.
