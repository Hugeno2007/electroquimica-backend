from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.rutas import api_router
from app.core.config import settings
from app.core.database import initialize_database


@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="ElectroQuímica API",
    description="API REST para la plataforma de monitoreo electroquímico.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", tags=["Sistema"])
def root():
    return {"service": "ElectroQuímica API", "docs": "/docs", "health": "/health"}

