import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from app.db.session import init_db
from app.services.ingestion_service import ingest_folder

if __name__=='__main__':
    init_db()
    print(ingest_folder())
