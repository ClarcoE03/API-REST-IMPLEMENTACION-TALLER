# API REST de Envíos

Versión: 1.0.0

Descripción
-----------
API REST para gestionar envíos, implementada con FastAPI y persistencia en PostgreSQL.
El proyecto incluye una configuración de desarrollo con Docker Compose para levantar
una base de datos PostgreSQL local.

Requisitos
----------
- Docker y Docker Compose
- Python 3.8+
- `pip`

Instalación rápida
------------------
1) Clona el repositorio y sitúate en la carpeta del proyecto:

```powershell
cd C:\ruta\a\ApiRest2
```

2) Levanta PostgreSQL (Docker Compose):

```powershell
docker-compose up -d
```

El contenedor `api_envios_db` expondrá PostgreSQL en el puerto `5432` con las credenciales por defecto:

- Usuario: `envios_user`
- Contraseña: `envios_password`
- Base de datos: `envios_db`

3) (Opcional) Crea un archivo `.env` a partir de `.env.example` si quieres cambiar la configuración.

4) Instala dependencias Python (recomendado usar un entorno virtual):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

5) Ejecuta la API con Uvicorn:

```powershell
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

Endpoints y uso
---------------
Base URL (local): `http://localhost:8080/api`

- `GET /envios` — Lista todos los envíos.
- `POST /envios` — Crea un envío (body JSON con `id`, `destinatario`, `direccion`, `estado`).
- `GET /envios/{id}` — Recupera un envío por `id`.
- `PUT /envios/{id}` — Actualiza campos de un envío (body parcial).
- `DELETE /envios/{id}` — Elimina un envío.

Documentación interactiva (Swagger UI): `http://localhost:8080/api/api-doc`

Ejemplos curl
-------------
Crear un envío:

```powershell
curl -X POST http://localhost:8080/api/envios -H "Content-Type: application/json" -d '{"id":"001","destinatario":"Juan Pérez","direccion":"Av. Siempre Viva 123","estado":"En tránsito"}'
```

Listar envíos:

```powershell
curl http://localhost:8080/api/envios
```

Obtener por id:

```powershell
curl http://localhost:8080/api/envios/001
```

Actualizar (PUT):

```powershell
curl -X PUT http://localhost:8080/api/envios/001 -H "Content-Type: application/json" -d '{"estado":"Entregado"}'
```

Eliminar:

```powershell
curl -X DELETE http://localhost:8080/api/envios/001
```

Base de datos
-------------
La tabla principal es `envios` con las columnas:

- `id` (varchar, PK)
- `destinatario` (varchar)
- `direccion` (varchar)
- `estado` (varchar)

La base de datos se inicializa automáticamente cuando arranca la aplicación (SQLAlchemy crea las tablas si no existen).

Despliegue y Docker
--------------------
Para detener los contenedores:

```powershell
docker-compose down
```

Para eliminar volúmenes (pérdida de datos):

```powershell
docker-compose down -v
```

Estructura del proyecto
-----------------------
```
ApiRest2/
├── app.py              # Aplicación FastAPI y rutas
├── database.py         # SQLAlchemy: engine, models, init_db
├── schemas.py          # Pydantic schemas
├── requirements.txt    # Dependencias Python
├── docker-compose.yml  # PostgreSQL
├── .env.example        # Variables de entorno de ejemplo
├── docs/               # Documentación y OpenAPI yaml
└── README.md           # Este archivo
```

Soporte y troubleshooting
-------------------------
- Si el puerto 8080 está ocupado: usa otro puerto `--port 8081` o mata el proceso que lo usa (`netstat -aon | findstr :8080` y `taskkill /PID <PID> /F`).
- Si la API no puede conectarse a la BD: verifica `docker-compose ps` y `docker-compose logs -f postgres`.
- Si necesitas resetear la BD: `docker-compose down -v` y `docker-compose up -d`.

Contribuciones
--------------
Si quieres mejorar la API (más campos, autenticación, tests), crea un fork y un PR. Puedo ayudar a añadir tests con `pytest` y un pipeline básico si lo deseas.

Licencia
--------
Proyecto de ejemplo — revisa con el propietario para añadir una licencia.

