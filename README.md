# HEATSHIFT

Local heat-aware work scheduling prototype using simulated workplace data.

## Backend

```powershell
cd backend
python -m pip install -r requirements.txt
python -m app.seed
python -m uvicorn app.main:app --reload --port 8000
```

## Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the frontend at http://localhost:5173.

API documentation: http://localhost:8000/docs

The project uses simulated data and is not medical software or a production safety system.
