# Documentación Técnica - Proyecto Videojuegos API

## 5. Arquitectura con Render

El proyecto implementa una arquitectura multi-contenedor utilizando Docker y Docker Compose, migrando de MySQL a PostgreSQL y manteniendo la separación entre aplicación y base de datos para mejorar la escalabilidad y el aislamiento.

**Componentes implementados:**
- **Contenedor de aplicación**: FastAPI con Python 3.11, expone el puerto 8000
- **Contenedor de base de datos**: PostgreSQL 16, almacenamiento persistente mediante volúmenes
- **Red Docker**: Comunicación interna entre contenedores mediante red bridge

**Configuración de la base de datos:**
- Host: `fastapi-db-postgres` (nombre del servicio en Docker Compose)
- Puerto interno: 5432
- Persistencia de datos mediante volumen nombrado `postgres_data`
- Variables de entorno para credenciales (usuario, contraseña, base de datos)

**Cambios realizados:**
- Migración de MySQL a PostgreSQL 16
- Cambio de driver de `pymysql` a `psycopg2-binary`
- Actualización de cadena de conexión a formato PostgreSQL
- Ajuste de puerto de 3306 a 5432

**Verificación:**
![alt text](videojuegos-db-punto4-1.png)