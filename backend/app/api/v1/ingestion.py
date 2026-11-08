from fastapi import APIRouter, HTTPException
from app.services.ingestion_service import ingest_folder
router = APIRouter(prefix='/ingestion',tags=['Ingestion'])


@router.post('/run')
def run_ingestion():
    try:
        return ingest_folder()
    except Exception as exc:
        raise HTTPException(status_code=500,detail=str(exc)) from exc
