# ANÁLISIS VIRTUAL IA — MVP

Aplicación inicial para analizar progreso y actividad de aprendizaje a partir de métricas proporcionadas por el usuario.

## Estado
- IMPLEMENTADO: API FastAPI con validación, análisis heurístico explicable y endpoint de salud.
- IMPLEMENTADO: interfaz web estática que consume la API.
- PENDIENTE: conectar un proveedor LLM real, autenticación, persistencia, despliegue y pruebas en CI.
- IMPORTANTE: las recomendaciones actuales son reglas deterministas; no se presentan como inferencia de un modelo entrenado.

## Arquitectura
```
Browser (HTML/CSS/JS)
        |
        | POST /api/analyze
        v
FastAPI + Pydantic
        |
        v
Analysis Engine (reglas transparentes)
        |
        v
Resumen + métricas + recomendaciones
```

## Ejecutar localmente
Requiere Python 3.12.

```bash
cd analisis-ia
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Abrir http://127.0.0.1:8000/ para la interfaz y http://127.0.0.1:8000/docs para la API.

## API
- `GET /api/health`
- `POST /api/analyze`

Ejemplo:
```json
{
  "subject": "Programación",
  "completed_tasks": 7,
  "total_tasks": 10,
  "errors": 3,
  "study_minutes": 90,
  "github_commits": 4
}
```

No enviar datos personales ni secretos. Las métricas deben ser autorizadas y no deben utilizarse por sí solas para decisiones académicas de alto impacto.
