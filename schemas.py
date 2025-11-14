from pydantic import BaseModel
from typing import Optional


class EnvioCreate(BaseModel):
    id: str
    destinatario: str
    direccion: str
    estado: str


class EnvioUpdate(BaseModel):
    destinatario: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[str] = None


class Envio(EnvioCreate):
    class Config:
        from_attributes = True
