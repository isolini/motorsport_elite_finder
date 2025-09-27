from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ...infraestrutura.db import session_scope
from ...models.models import TelemetrySample, Sessao

router = APIRouter(prefix="/telemetria", tags=["telemetria"])

# ---------- Schemas ----------

class TelemetriaIn(BaseModel):
    sessao_id: int
    ts: Optional[datetime] = None
    rpm: Optional[int] = Field(default=None, ge=0)
    coolant_temp: Optional[float] = None
    speed: Optional[float] = None
    throttle: Optional[float] = None
    brake: Optional[float] = None
    gear: Optional[int] = None

class TelemetriaOut(BaseModel):
    id: int
    sessao_id: int
    ts: datetime
    rpm: Optional[int]
    coolant_temp: Optional[float]
    speed: Optional[float]
    throttle: Optional[float]
    brake: Optional[float]
    gear: Optional[int]

    class Config:
        # Pydantic v2: permite construir o modelo a partir de objetos ORM
        from_attributes = True

class BatchResult(BaseModel):
    inserted: int

# ---------- Endpoints ----------

@router.post("/batch", response_model=BatchResult)
def inserir_batch(amostras: List[TelemetriaIn]):
    if not amostras:
        return {"inserted": 0}

    with session_scope() as s:
        # valida se TODAS as sessoes existem
        sessao_ids = {a.sessao_id for a in amostras}
        count_sessoes = s.query(Sessao).filter(Sessao.id.in_(list(sessao_ids))).count()
        if count_sessoes != len(sessao_ids):
            raise HTTPException(status_code=400, detail="sessao_id inválido em uma ou mais amostras")

        for a in amostras:
            sample = TelemetrySample(
                sessao_id=a.sessao_id,
                ts=a.ts or datetime.utcnow(),
                rpm=a.rpm,
                coolant_temp=a.coolant_temp,
                speed=a.speed,
                throttle=a.throttle,
                brake=a.brake,
                gear=a.gear,
            )
            s.add(sample)

        # commit acontece no session_scope
        return {"inserted": len(amostras)}

@router.get("/ultimas", response_model=List[TelemetriaOut])
def ultimas(sessao_id: int = Query(...), limit: int = Query(5, ge=1, le=100)):
    with session_scope() as s:
        rows = (
            s.query(TelemetrySample)
            .filter(TelemetrySample.sessao_id == sessao_id)
            .order_by(TelemetrySample.ts.desc())
            .limit(limit)
            .all()
        )
        # Pydantic v2: converter ORM -> schema explicitamente
        return [TelemetriaOut.model_validate(r, from_attributes=True) for r in rows]
