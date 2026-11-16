# Page Tracker

A small Flask web service that counts page views in **Redis**. The app is deliberately simple. The point of the project is the **engineering around it**: a layered test suite, a linted and security-scanned multi-stage Docker build, and a CI pipeline that tests end to end and publishes the image to Docker Hub.

Built while following the Real Python tutorial on Docker and GitHub Actions CI/CD.

## What it does

```
GET /  →  "This page has been seen 5 times."
```

Each request atomically increments a Redis counter. If Redis is unavailable, the service logs the error and returns a `500` with a friendly message.

## Architecture

```
            docker compose
   ┌──────────────────────────────────┐
   │  web-service (gunicorn + Flask)  │──► redis-service (Redis 7, persistent volume)
   └──────────────────────────────────┘
        ▲
        └── test-service (pytest e2e, runs only with the `testing` profile)
```

## Quality gates

The multi-stage `Dockerfile` **fails the build** unless all of these pass:

- Unit tests (`pytest`)
- Linting and style: `flake8`, `isort`, `black`, `pylint`
- Security scan: `bandit`

The final image is slim, installs only the built wheel, and runs as a non-root user.

### Test suite

| Level | Location | What it covers |
|---|---|---|
| Unit | `web/test/unit/` | Route logic with Redis mocked |
| Integration | `web/test/integration/` | App against a real Redis |
| End-to-end | `web/test/e2e/` | HTTP requests against the running containers |

## CI/CD

`.github/workflows/ci.yml` runs on every push and PR to `main`:

1. Builds the images and runs the end-to-end tests with `docker compose --profile testing up`.
2. On pushes to `main`, logs in to Docker Hub and publishes `page-tracker:<commit-sha>` and `page-tracker:latest`.

## Getting started

**Prerequisites:** Docker with Compose v2.

```bash
git clone https://github.com/lumosityfan/page-tracker.git
cd page-tracker

docker compose up --build        # app on http://localhost
curl http://localhost            # → This page has been seen 1 times.
```

Run the end-to-end tests:

```bash
docker compose --profile testing up --build --exit-code-from test-service
```

## Tech stack

Python 3.11 · Flask · Gunicorn · Redis · Docker / Docker Compose · pytest · GitHub Actions

## Credits

Based on the Real Python tutorial *Build a Docker image and CI/CD pipeline for a Flask app*.
