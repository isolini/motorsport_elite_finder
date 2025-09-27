# src/projeto/api/routers/db_router.py
from fastapi import APIRouter
from sqlalchemy import text

from ...infraestrutura.db import session_scope

router = APIRouter(prefix="/db", tags=["db"])

@router.get("/ping")
def ping():
    # simples SELECT 1 pra validar a conexão
    with session_scope() as s:
        s.execute(text("SELECT 1"))
    return {"status": "ok"}
