# Veterinaria Backend (Flask)

Este proyecto es el backend de un sistema de gestión veterinaria, desarrollado con Flask y MySQL. Permite gestionar mascotas, clientes, citas, historial clínico, usuarios y servicios.

## Estructura del Proyecto

```
vet/
├── app/                # Código fuente del backend Flask
├── migrations/         # Archivos de migración de base de datos (Alembic)
├── .venv/              # Entorno virtual Python (NO subir a Git)
├── README.md           # Este archivo
└── ...
```

## Requisitos

- Python 3.12+
- MySQL Server (instalado y corriendo)
- pip

## Instalación y configuración

1. **Crea y activa un entorno virtual** (desde la raíz del proyecto):

   ```sh
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instala las dependencias:**

   ```sh
   pip install -r app/requirements.txt
   ```

3. **Configura la base de datos MySQL:**
   - Crea una base de datos en MySQL, por ejemplo:
     ```sql
     CREATE DATABASE veterinaria_db;
     ```
   - Edita `app/config.py` si necesitas cambiar el usuario, contraseña o nombre de la base de datos.

4. **Realiza las migraciones de la base de datos:**

   ```sh
   flask db upgrade
   ```
   Si no tienes el comando `flask`, puedes correrlo así:
   ```sh
   python -m flask db upgrade
   ```

## Ejecución

> **Importante:**  
> Activa el entorno virtual desde la raíz del proyecto (`vet`), pero ejecuta el backend desde la raíz también.

1. Activa el entorno virtual:
   ```sh
   # Desde la raíz del proyecto
   .venv\Scripts\activate   # En Windows
   # source .venv/bin/activate   # En Linux/Mac
   ```

2. Inicia el backend:
   ```sh
   python -m app.main
   ```
   El backend estará disponible en [http://localhost:5000](http://localhost:5000).

## Crear un usuario admin manualmente

Para crear un usuario administrador desde la terminal:

1. Asegúrate de que la base de datos esté creada y migrada.
2. Ejecuta el script:
   ```sh
   python -m app.scripts.create_admin
   ```
   El script te pedirá el nombre de usuario, email y contraseña para el admin.

## Endpoints principales

Consulta el archivo [`app/routes.py`](app/routes.py) para ver todos los endpoints disponibles.

## Notas

- **No subas la carpeta `.venv` ni archivos de configuración sensibles a GitHub.**
- Si tienes problemas de importación, asegúrate de estar en la raíz del proyecto y de que el entorno virtual esté activado.

---
