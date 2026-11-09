from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="ANÁLISIS VIRTUAL IA",
    version="0.1.0",
    description="MVP de analítica de aprendizaje con recomendaciones explicables.",
)

class AnalysisInput(BaseModel):
    subject: str = Field(default="General", min_length=1, max_length=100)
    completed_tasks: int = Field(ge=0, le=100000)
    total_tasks: int = Field(ge=1, le=100000)
    errors: int = Field(default=0, ge=0, le=100000)
    study_minutes: int = Field(default=0, ge=0, le=1000000)
    github_commits: int = Field(default=0, ge=0, le=100000)

class AnalysisOutput(BaseModel):
    subject: str
    completion_percent: float
    error_count: int
    study_minutes: int
    activity_signal: str
    level: str
    findings: List[str]
    recommendations: List[str]
    method: str

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "analisis-virtual-ia", "version": "0.1.0"}

@app.post("/api/analyze", response_model=AnalysisOutput)
def analyze(data: AnalysisInput):
    # Reject inconsistent input rather than silently producing misleading metrics.
    completed = min(data.completed_tasks, data.total_tasks)
    completion = round((completed / data.total_tasks) * 100, 1)

    findings = []
    recommendations = []

    if completion >= 80:
        level = "Avance alto"
        findings.append("La proporción de tareas completadas es igual o superior al 80%.")
        recommendations.append("Continúa con el siguiente objetivo y valida la calidad de los resultados.")
    elif completion >= 50:
        level = "Avance intermedio"
        findings.append("Se ha completado al menos la mitad de las tareas.")
        recommendations.append("Divide las tareas pendientes en pasos pequeños y prioriza una por sesión.")
    else:
        level = "Necesita seguimiento"
        findings.append("Menos de la mitad de las tareas están completadas.")
        recommendations.append("Revisa los bloqueos y comienza por una tarea breve y verificable.")

    if data.errors > 5:
        findings.append("Se registran más de cinco errores en la actividad reportada.")
        recommendations.append("Clasifica los errores por causa y repite una práctica enfocada.")
    elif data.errors > 0:
        findings.append("Hay errores registrados; el número por sí solo no determina el dominio.")
        recommendations.append("Revisa los errores y documenta qué corrección resolvió cada uno.")
    else:
        findings.append("No se reportaron errores en esta medición.")

    if data.study_minutes < 30:
        activity = "Actividad breve"
        recommendations.append("Si es posible, programa una sesión adicional y registra su resultado.")
    else:
        activity = "Actividad registrada"
    if data.github_commits:
        findings.append(f"Se reportaron {data.github_commits} commits de GitHub; esto mide actividad, no calidad del código.")

    return AnalysisOutput(
        subject=data.subject,
        completion_percent=completion,
        error_count=data.errors,
        study_minutes=data.study_minutes,
        activity_signal=activity,
        level=level,
        findings=findings,
        recommendations=recommendations,
        method="Reglas deterministas explicables; no utiliza un modelo generativo ni evalúa personas.",
    )

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def home():
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"message": "ANÁLISIS VIRTUAL IA", "docs": "/docs"}
