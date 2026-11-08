from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.db.session import init_db
from app.api.v1 import ingestion,resumes,jobs,matching,generation


@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield


app=FastAPI(title='Resume Intelligence API',version='0.1.0',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=[s.strip() for s in get_settings().cors_origins.split(',')],allow_credentials=False,allow_methods=['GET','POST'],allow_headers=['Content-Type'])
for router in [ingestion.router,resumes.router,jobs.router,matching.router,generation.router]:
    app.include_router(router,prefix='/api/v1')


@app.get('/health')
def health():
    return {'status':'ok'}
