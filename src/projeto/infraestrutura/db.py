# src/projeto/infraestrutura/db.py
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # dotenv é opcional; se não estiver instalado, seguimos com variáveis do ambiente
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Para SQLite local, precisamos do check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

@contextmanager
def session_scope() -> Generator:
    """Abre uma sessão do SQLAlchemy e garante fechamento/rollback adequado."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
