# src/projeto/models/models.py
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Float, Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} email={self.email}>"

class Sessao(Base):
    __tablename__ = "sessoes"

    id = Column(Integer, primary_key=True, index=True)
    driver_name = Column(String(120), nullable=False)
    track_name = Column(String(120), nullable=False)
    vehicle = Column(String(120), nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)

    samples = relationship("TelemetrySample", back_populates="sessao", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Sessao id={self.id} driver={self.driver_name} track={self.track_name}>"

class TelemetrySample(Base):
    __tablename__ = "telemetry_samples"

    id = Column(Integer, primary_key=True, index=True)
    sessao_id = Column(Integer, ForeignKey("sessoes.id"), nullable=False, index=True)
    ts = Column(DateTime, default=datetime.utcnow, nullable=False)

    # campos básicos pro MVP
    rpm = Column(Integer, nullable=True)
    coolant_temp = Column(Float, nullable=True)

    # extras comuns (opcional usar agora)
    speed = Column(Float, nullable=True)
    throttle = Column(Float, nullable=True)
    brake = Column(Float, nullable=True)
    gear = Column(Integer, nullable=True)

    sessao = relationship("Sessao", back_populates="samples")

# índices úteis
Index("ix_samples_sessao_ts", TelemetrySample.sessao_id, TelemetrySample.ts)
Index("ix_samples_sessao_rpm", TelemetrySample.sessao_id, TelemetrySample.rpm)
