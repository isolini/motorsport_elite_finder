from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from ...infraestrutura.db import session_scope
from ...models.models import Sessao

router = APIRouter(prefix="/sessoes", tags=["sessoes"])

class SessaoCreate(BaseModel):
    driver_name: str = Field(..., min_length=1)
    track_name: str = Field(..., min_length=1)
    vehicle: Optional[str] = None

class SessaoOut(BaseModel):
    id: int
    driver_name: str
    track_name: str
    vehicle: Optional[str] = None

    class Config:
        from_attributes = True  # v2

@router.post("", response_model=SessaoOut, status_code=201)
def criar_sessao(payload: SessaoCreate):
    with session_scope() as s:
        sess = Sessao(
            driver_name=payload.driver_name,
            track_name=payload.track_name,
            vehicle=payload.vehicle,
        )
        s.add(sess)
        s.flush()
        # esta linha é a chave: converte ORM -> Pydantic v2
        return SessaoOut.model_validate(sess, from_attributes=True)
