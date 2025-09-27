import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from ..infraestrutura.db import engine
from ..models.models import Base

from .routers.db_router import router as db_router
from .routers.sessoes_router import router as sessoes_router
from .routers.telemetria_router import router as telemetria_router

# Carregar variáveis de ambiente (opcional)
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

API_PREFIX = os.getenv("API_PREFIX", "/api")

# Caminho absoluto para a pasta de arquivos estáticos (front SPA)
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# ---------- Lifespan para startup/shutdown ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executado no startup
    Base.metadata.create_all(bind=engine)
    yield
    # Aqui poderia ir código de shutdown se necessário

# ---------- App ----------
app = FastAPI(
    title="Motorsport API - Semana 9 (SQLite)",
    lifespan=lifespan
)

# Rotas da API (sempre com prefixo /api)
app.include_router(db_router, prefix=API_PREFIX)
app.include_router(sessoes_router, prefix=API_PREFIX)
app.include_router(telemetria_router, prefix=API_PREFIX)

# Endpoint simples para status da API
@app.get(API_PREFIX + "/status")
def api_status():
    return {"status": "ok", "api": API_PREFIX}

# Servir o front-end estático (SPA) em "/"
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
