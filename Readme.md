# flask-cicd-api

A production-grade Python Flask REST API built to demonstrate end-to-end ownership of backend systems, containerization, CI/CD pipelines, and dual-cloud deployment across AWS and Azure.

---

## What This Project Demonstrates

- Designing and running a REST API with proper error handling and structured logging
- Containerizing an application with Docker using production best practices
- Owning a CI/CD pipeline that tests and builds automatically on every push
- Deploying to AWS using ECR and App Runner with IAM authentication
- Deploying the same image to Azure using ACR and Container Apps with Log Analytics
- Running a production WSGI server (Gunicorn) instead of a development server

---

## Live Deployments

| Cloud | URL |
|-------|-----|
| AWS App Runner | https://6tijravw6a.us-east-1.awsapprunner.com |
| Azure Container Apps | https://flask-cicd-app.ashyfield-c85e30e9.eastus.azurecontainerapps.io |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check with UTC timestamp |
| GET | `/api/v1/records` | Returns all records |
| GET | `/api/v1/records/<id>` | Returns a single record |

### Example Response - Health Check

```json
{
  "status": "healthy",
  "time": "2026-02-27T14:47:15.129610+00:00"
}
```

### Example Response - Records

```json
{
  "data": [
    { "id": 1, "name": "Biomass Site A", "value": 4200 },
    { "id": 2, "name": "Biomass Site B", "value": 3800 }
  ],
  "count": 2
}
```

### Example Response - 404 Error

```json
{
  "error": "Record not found"
}
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Runtime |
| Flask 3.1 | Web framework |
| Gunicorn | Production WSGI server |
| Docker | Containerization |
| GitHub Actions | CI pipeline |
| AWS ECR | Container registry on AWS |
| AWS App Runner | Managed deployment on AWS |
| Azure ACR | Container registry on Azure |
| Azure Container Apps | Managed deployment on Azure |
| Azure Log Analytics | Production log collection |
| Pytest | Automated testing |

---

## Project Structure

```
flask-cicd-api/
    app.py                        # Flask application
    test_app.py                   # Pytest test suite
    requirements.txt              # Pinned dependencies
    Dockerfile                    # Container build instructions
    .dockerignore                 # Docker exclusions
    .gitignore                    # Git exclusions
    .github/
        workflows/
            ci.yml                # GitHub Actions CI pipeline
```

---

## CI/CD Pipeline

Every push to the `main` branch automatically triggers the GitHub Actions pipeline which:

1. Sets up Python 3.12
2. Installs all dependencies from requirements.txt
3. Runs the full test suite with Pytest
4. Builds the Docker image

If any step fails, the pipeline fails and the issue must be resolved before merging.

---

## Running Locally

### Prerequisites

- Python 3.12
- Docker Desktop
- Git

### Setup

```bash
git clone https://github.com/LeonardKachi/flask-cicd-api.git
cd flask-cicd-api
virtualenv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Run the API

```bash
python app.py
```

API available at `http://localhost:5000`

### Run with Docker

```bash
docker build -t flask-cicd-api .
docker run -p 5000:5000 flask-cicd-api
```

### Run Tests

```bash
pytest --tb=short
```

---

## Deployment Architecture

### AWS

```
GitHub Push
    → GitHub Actions (test + build)
    → Docker build
    → Push image to AWS ECR
    → AWS App Runner pulls latest image
    → Live on public HTTPS URL
```

### Azure

```
GitHub Push
    → GitHub Actions (test + build)
    → Docker build
    → Push image to Azure ACR
    → Azure Container Apps pulls latest image
    → Live on public HTTPS URL
    → Logs flowing to Azure Log Analytics
```

---

## Production Decisions

**Gunicorn over Flask dev server** - Flask's built-in server is single-threaded and not safe for production. Gunicorn runs multiple worker processes and handles concurrent requests properly.

**Structured logging** - Every request logs method, path, status code, and IP. This makes debugging production issues possible without guessing.

**Layer-optimized Dockerfile** - Dependencies are copied and installed before application code. This means Docker reuses the dependency layer on rebuilds unless requirements.txt changes, making builds faster.

**Pinned dependencies** - requirements.txt uses exact versions to ensure the environment is reproducible across any machine or deployment target.

**Health check endpoint** - Every production system needs a health check. Load balancers, orchestrators, and monitoring tools use this to verify the service is alive.

---

## Author

Onyedikachi Henry Leonard
[GitHub](https://github.com/LeonardKachi) | [LinkedIn](https://linkedin.com/in/onyedikachi-leonard)