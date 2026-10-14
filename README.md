# HEATSHIFT

Local Round 2 MVP prototype for heat-aware work scheduling.

## Module 1 setup

### Backend

```powershell
cd backend
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Health check: http://localhost:8000/api/health

### Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The page reports whether the FastAPI backend is connected.

Modules 1–7 provide the React/Vite and FastAPI foundation, SQLite demo data, deterministic heat-burden calculations, scheduling, API workflow, dashboard, and demo polish. Live integrations and production deployment are intentionally not included.

## Module 2 database

After installing backend requirements, from `backend` run:

```powershell
python -m app.seed
```

This creates `backend/heatshift.db` with repeatable simulated Dhaka garment-factory data. To reset and reseed, run the same command again. The read-only scenario endpoint is available at http://localhost:8000/api/demo/scenario.

Module 3 adds the deterministic heat-burden endpoint at http://localhost:8000/api/demo/heat-burden and unit tests via `python -m unittest discover tests` from `backend`.

Module 4 adds `POST http://localhost:8000/api/schedule/recommend` with `{ "transfer_locked": false }` for a feasible recommendation or `true` for the no-safe-schedule scenario.

Module 5 exposes the frontend workflow endpoints: `/api/demo/original-schedule`, `/api/demo/heat-timeline`, and `POST /api/demo/what-if`. Interactive API documentation is available at http://localhost:8000/docs.

## Module 7 demo polish

Presenter notes are in [PRESENTER_NOTES.md](PRESENTER_NOTES.md). The required disclaimer is shown in the dashboard and API responses. The app is designed to run offline after dependencies are installed and uses no cloud APIs, sensors, or live language model.
