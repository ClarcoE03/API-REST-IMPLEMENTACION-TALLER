# API REST de Envíos con PostgreSQL

## Descripción
API REST desarrollada con FastAPI para gestionar envíos. Los datos se persisten en una base de datos PostgreSQL levantada en Docker.

## Requisitos
- Docker y Docker Compose
- Python 3.8+
- pip

## Instalación y Ejecución

### 1. Levantar PostgreSQL con Docker Compose
```powershell
docker-compose up -d
```

Esto levantará un contenedor de PostgreSQL en el puerto `5432` con:
- Usuario: `envios_user`
- Contraseña: `envios_password`
- BD: `envios_db`

Para verificar que el contenedor está activo:
```powershell
docker ps | findstr api_envios_db
# o
docker-compose ps
```

Para ver los logs:
```powershell
docker-compose logs -f postgres
```

### 2. Instalar dependencias Python
```powershell
python -m pip install -r requirements.txt
```

### 3. Ejecutar la API
```powershell
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

La API estará disponible en:
- **Documentación Swagger**: http://localhost:8080/api/api-doc
- **OpenAPI JSON**: http://localhost:8080/api/openapi.json

## Endpoints

### GET /api/envios
Listar todos los envíos desde la BD.

### POST /api/envios
Crear un nuevo envío.
```json
{
  "id": "002",
  "destinatario": "María García",
  "direccion": "Calle Principal 456",
  "estado": "Pendiente"
}
```

### GET /api/envios/{id}
Obtener un envío por su ID.

### PUT /api/envios/{id}
Actualizar un envío existente.
```json
{
  "estado": "Entregado"
}
```

### DELETE /api/envios/{id}
Eliminar un envío.

## Parar los contenedores
```powershell
docker-compose down
```

Para eliminar volúmenes de datos:
```powershell
docker-compose down -v
```

## Estructura del Proyecto
```
ApiRest2/
├── app.py                  # Aplicación principal (FastAPI)
├── database.py             # Configuración y modelos SQLAlchemy
├── schemas.py              # Esquemas Pydantic
├── requirements.txt        # Dependencias Python
├── docker-compose.yml      # Configuración de PostgreSQL en Docker
├── .env.example            # Variables de entorno (ejemplo)
└── README.md               # Este archivo
```
