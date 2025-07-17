# Veterinaria Backend (Flask)

Este proyecto es el backend de un sistema de gestión veterinaria, desarrollado con Flask y MySQL. Permite gestionar mascotas, clientes, citas, historial clínico, usuarios y servicios.

## Estructura del Proyecto

```
app/
├── __init__.py           # Inicialización y configuración principal de Flask
├── config.py             # Configuración de entornos y base de datos
├── controllers.py        # Lógica de negocio y funciones auxiliares
├── main.py               # Punto de entrada para ejecutar el backend
├── models.py             # Modelos de base de datos (SQLAlchemy)
├── routes.py             # Rutas y endpoints de la API REST
├── utils.py              # Funciones utilitarias para respuestas estándar
├── requirements.txt      # Dependencias de Python
├── .gitignore            # Archivos y carpetas a ignorar en Git
├── README.md             # Este archivo
├── scripts/
│   └── create_admin.py   # Script para crear un usuario admin manualmente
├── migrations/           # Archivos de migración de base de datos (Alembic)
└── instance/             # Configuración específica de instancia (NO subir)
```


1. ## Requisitos

- Python 3.12+
- MySQL Server (instalado y corriendo)
- pip


2. **Crea y activa un entorno virtual:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate   # En Windows
   # source .venv/bin/activate   # En Linux/Mac
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configura la base de datos MySQL:**
   - Crea una base de datos en MySQL, por ejemplo:
     ```sql
     CREATE DATABASE veterinaria_db 
     ```
   - Edita `config.py` si necesitas cambiar el usuario, contraseña o nombre de la base de datos.

5. **Realiza las migraciones de la base de datos:**
   ```sh
   flask db upgrade
   ```
   Si no tienes el comando `flask`, puedes correrlo así:
   ```sh
   python -m flask db upgrade
   ```

## Ejecución

**Importante:**  
Para evitar errores de importación, activa el entorno virtual dentro de la carpeta `app`, pero ejecuta el backend desde la raíz del proyecto (`vet`):

1. Activa el entorno virtual:
   ```sh
   cd app
   .\.venv\Scripts\activate   # En Windows
   ```

2. Regresa a la raíz del proyecto:
   ```sh
   cd ..
   ```

3. Inicia el backend con:
   ```sh
   python -m app.main
   ```
   El backend estará disponible en [http://localhost:5000](http://localhost:5000).

## Crear un usuario admin manualmente

Para crear un usuario administrador desde la terminal:

1. Asegúrate de que la base de datos esté creada y migrada.
2. Ejecuta el script:
   ```sh
   python app/scripts/create_admin.py
   ```
   El script te pedirá el nombre de usuario, email y contraseña para el admin.

## Endpoints principales

Consulta el archivo [`routes.py`](routes.py) para ver todos los endpoints disponibles.

