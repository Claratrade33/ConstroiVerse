# Project Architecture Skeleton

## Backend (Flask API)
- `backend/app.py` – application entry point
- `backend/controllers/` – request handlers grouped by domain
- `backend/models/` – data schemas and database logic
- `backend/services/` – business rules and integrations
- `backend/utils/` – shared helpers
- `backend/tests/` – unit tests for backend components

## Frontend (Web Client)
- `frontend/` – root for web assets
  - `frontend/src/` – JavaScript modules and components
  - `frontend/public/` – static files
  - `frontend/tests/` – frontend tests

## Shared
- `docs/` – project documentation and planning
- `requirements.txt` – Python dependencies
- `package.json` – frontend dependencies
- `render.yaml` / `Procfile` – deployment configuration
