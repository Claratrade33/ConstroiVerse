from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

engine_kwargs = {"pool_pre_ping": True, "future": True}
# Para SQLite em dev evitar erros de thread
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    # importar modelos para que as tabelas existam
    from backend.models.user import User  # noqa
    from backend.models.obra import Obra  # noqa
    from backend.models.orcamento import Orcamento  # noqa
    Base.metadata.create_all(bind=engine)