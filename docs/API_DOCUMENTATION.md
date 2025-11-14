# Documentación del proyecto: API REST de Envíos

Versión: 1.0.0

Índice
- Descripción
- Requisitos
- Variables de entorno
- Levantar la infraestructura (Docker + PostgreSQL)
- Instalar dependencias Python
- Ejecutar la API
- Endpoints (detallados)
  - GET /api/envios
  - POST /api/envios
  - GET /api/envios/{id}
  - PUT /api/envios/{id}
  - DELETE /api/envios/{id}
- Esquema de la base de datos
- Ejemplos con `curl`
- Comprobaciones y troubleshooting
- Ficheros importantes

---

## Descripción

API REST para gestionar envíos. Implementada con FastAPI y persistencia en PostgreSQL. El proyecto incluye un `docker-compose.yml` que levanta PostgreSQL.

## Requisitos

- Docker y Docker Compose
- Python 3.8+
- pip
- (Opcional) Postman

## Variables de entorno

Puedes crear un `.env` a partir de `.env.example`. Variables relevantes:

- `DATABASE_URL` - URL de conexión a PostgreSQL (ejemplo: `postgresql://envios_user:envios_password@localhost:5432/envios_db`)
- `API_HOST` - host donde corre la API (por defecto `0.0.0.0`)
- `API_PORT` - puerto de la API (por defecto `8080`)

## Levantar la infraestructura

En la raíz del proyecto ejecuta:

```powershell
docker-compose up -d
```

Esto levantará:
- Contenedor `api_envios_db` (PostgreSQL 15)

Comprueba que el contenedor está en estado `healthy`:

```powershell
docker ps
# o
docker-compose ps
```

## Instalar dependencias Python

```powershell
python -m pip install -r requirements.txt
```

## Ejecutar la API

```powershell
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

La documentación interactiva está en:

- Swagger UI: `http://localhost:8080/api/api-doc`
- OpenAPI JSON: `http://localhost:8080/api/openapi.json`

---

## Endpoints (detallados)

Todos los endpoints tienen prefijo `/api`.

### GET /api/envios
- Descripción: Lista todos los envíos almacenados en la base de datos.
- Respuesta: `200 OK`
- Body (ejemplo):

```json
[
  {
    "id": "001",
    "destinatario": "Juan Pérez",
    "direccion": "Av. Siempre Viva 123",
    "estado": "En tránsito"
  }
]
```

### POST /api/envios
- Descripción: Crea un nuevo envío. El campo `id` debe ser único.
- Request body (JSON):

```json
{
  "id": "002",
  "destinatario": "María Garcia",
  "direccion": "Calle Principal 456",
  "estado": "Pendiente"
}
```

- Respuestas:
  - `201 Created` / `200 OK`: devuelve el objeto creado (según implementación actual devuelve `200`)
  - `400 Bad Request`: si ya existe un envío con ese `id`.

- Body (ejemplo respuesta exitosa):

```json
{
  "id": "002",
  "destinatario": "María Garcia",
  "direccion": "Calle Principal 456",
  "estado": "Pendiente"
}
```

### GET /api/envios/{id}
- Descripción: Recupera un envío por su `id`.
- Parámetros:
  - `id` (path) - identificador del envío
- Respuestas:
  - `200 OK`: devuelve el envío
  - `404 Not Found`: si no existe

- Body (ejemplo):
```json
{
  "id": "001",
  "destinatario": "Juan Pérez",
  "direccion": "Av. Siempre Viva 123",
  "estado": "En tránsito"
}
```

### PUT /api/envios/{id}
- Descripción: Actualiza campos del envío con `id`.
- Request body (parcial) (JSON):

```json
{
  "destinatario": "Nuevo Nombre",
  "direccion": "Nueva Dirección",
  "estado": "Entregado"
}
```

- Respuestas:
  - `200 OK`: devuelve el recurso actualizado
  - `404 Not Found`: si no existe

### DELETE /api/envios/{id}
- Descripción: Elimina el envío con `id`.
- Respuestas:
  - `200 OK`: confirmación de eliminación
  - `404 Not Found`: si no existe

- Body (ejemplo):
```json
{ "mensaje": "Envío 001 eliminado correctamente" }
```

---

## Esquema de la base de datos

Tabla: `envios`

- `id` VARCHAR PRIMARY KEY
- `destinatario` VARCHAR
- `direccion` VARCHAR
- `estado` VARCHAR

SQL de creación (generado por SQLAlchemy, ejemplo equivalente):

```sql
CREATE TABLE envios (
  id varchar PRIMARY KEY,
  destinatario varchar,
  direccion varchar,
  estado varchar
);
```

---

## Ejemplos con curl

- Crear envío:

```bash
curl -X POST http://localhost:8080/api/envios \
  -H 'Content-Type: application/json' \
  -d '{"id":"010","destinatario":"Prueba","direccion":"Calle 1","estado":"Pendiente"}'
```

- Listar envíos:

```bash
curl http://localhost:8080/api/envios
```

- Obtener envío por id:

```bash
curl http://localhost:8080/api/envios/010
```

- Actualizar envío:

```bash
curl -X PUT http://localhost:8080/api/envios/010 \
  -H 'Content-Type: application/json' \
  -d '{"estado":"Entregado"}'
```

- Eliminar envío:

```bash
curl -X DELETE http://localhost:8080/api/envios/010
```

---

## Comprobaciones y troubleshooting

- Si la API no arranca por error de conexión a BD: verifica que Docker Compose esté levantado y que `DATABASE_URL` apunte a `localhost:5432` o al host correcto.
- Si el puerto 8080 está en uso: cambia el puerto o detén el proceso que lo ocupa (`netstat -aon | findstr :8080` y `taskkill /PID <PID> /F`).

---

## Ficheros importantes

- `app.py` — aplicación FastAPI
- `database.py` — configuración y modelos SQLAlchemy
- `schemas.py` — esquemas Pydantic
- `docker-compose.yml` — PostgreSQL
- `requirements.txt` — dependencias
- `README.md` — guía rápida
- `docs/openapi.yaml` — especificación OpenAPI (generada)

---

Si quieres que además genere un archivo `docs/openapi.yaml` (OpenAPI 3.0) listo para importar en Postman o SwaggerHub, dime y lo incluyo.