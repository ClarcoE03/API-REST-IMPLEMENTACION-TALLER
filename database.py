from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://envios_user:envios_password@localhost:5432/envios_db"
)

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Envio(Base):
    __tablename__ = "envios"

    id = Column(String, primary_key=True, index=True)
    destinatario = Column(String, index=True)
    direccion = Column(String)
    estado = Column(String)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Crear las tablas en la BD si no existen"""
    Base.metadata.create_all(bind=engine)
