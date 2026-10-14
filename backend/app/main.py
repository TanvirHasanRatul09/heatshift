from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.scenario import router as scenario_router
from .api.schedule import router as schedule_router
from .api.demo import router as demo_router

app = FastAPI(title="HEATSHIFT API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(scenario_router)
app.include_router(schedule_router)
app.include_router(demo_router)

@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
