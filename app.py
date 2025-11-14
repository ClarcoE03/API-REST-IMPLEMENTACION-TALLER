from fastapi import FastAPI, APIRouter, Path, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import init_db, get_db, Envio as EnvioDB
from schemas import Envio, EnvioCreate, EnvioUpdate

app = FastAPI(
    title="API de Envíos",
    version="1.0.0",
    description="API REST para registrar y consultar envíos",
    openapi_url="/api/openapi.json",
    docs_url="/api/api-doc",
    redoc_url=None,
)

router = APIRouter(prefix="/api")


@app.on_event("startup")
def startup_event():
    """Inicializar la BD al arrancar la app"""
    init_db()
    print("✓ Base de datos inicializada")


@router.get("/envios", response_model=List[Envio])
def listar_envios(db: Session = Depends(get_db)):
    """Listar todos los envíos desde la BD."""
    envios = db.query(EnvioDB).all()
    return envios


@router.post("/envios", response_model=Envio)
def crear_envio(envio: EnvioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo envío en la BD."""
    # Verificar si el ID ya existe
    db_envio = db.query(EnvioDB).filter(EnvioDB.id == envio.id).first()
    if db_envio:
        raise HTTPException(status_code=400, detail="El envío con este ID ya existe")
    
    # Crear nuevo envío
    nuevo_envio = EnvioDB(
        id=envio.id,
        destinatario=envio.destinatario,
        direccion=envio.direccion,
        estado=envio.estado
    )
    db.add(nuevo_envio)
    db.commit()
    db.refresh(nuevo_envio)
    return nuevo_envio


@router.get("/envios/{envio_id}", response_model=Envio)
def obtener_envio(envio_id: str = Path(..., description="ID del envío"), db: Session = Depends(get_db)):
    """Obtener un envío por su ID desde la BD."""
    envio = db.query(EnvioDB).filter(EnvioDB.id == envio_id).first()
    if not envio:
        raise HTTPException(status_code=404, detail=f"Envío con ID {envio_id} no encontrado")
    return envio


@router.put("/envios/{envio_id}", response_model=Envio)
def actualizar_envio(envio_id: str, envio_update: EnvioUpdate, db: Session = Depends(get_db)):
    """Actualizar un envío existente en la BD."""
    envio = db.query(EnvioDB).filter(EnvioDB.id == envio_id).first()
    if not envio:
        raise HTTPException(status_code=404, detail=f"Envío con ID {envio_id} no encontrado")
    
    if envio_update.destinatario is not None:
        envio.destinatario = envio_update.destinatario
    if envio_update.direccion is not None:
        envio.direccion = envio_update.direccion
    if envio_update.estado is not None:
        envio.estado = envio_update.estado
    
    db.commit()
    db.refresh(envio)
    return envio


@router.delete("/envios/{envio_id}")
def eliminar_envio(envio_id: str, db: Session = Depends(get_db)):
    """Eliminar un envío de la BD."""
    envio = db.query(EnvioDB).filter(EnvioDB.id == envio_id).first()
    if not envio:
        raise HTTPException(status_code=404, detail=f"Envío con ID {envio_id} no encontrado")
    
    db.delete(envio)
    db.commit()
    return {"mensaje": f"Envío {envio_id} eliminado correctamente"}


app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, log_level="info")
