# Veterinaria - Sistema de Gestión

Este repositorio contiene el sistema completo de gestión veterinaria, incluyendo el backend (Flask + MySQL) y el frontend (Vue 3 + Vite).

## Estructura del Proyecto

```
vet/
├── app/         # Backend Flask (API y lógica de negocio)
├── frontend/    # Frontend Vue (interfaz de usuario)
├── README.md    # Este archivo (instrucciones generales)
```

## Requisitos Generales

- Python 3.12+ (para el backend)
- MySQL Server (para la base de datos)
- Node.js 18+ y npm 9+ (para el frontend)

---

## Instalación Rápida

### 1. Clona el repositorio

```sh
git clone <URL_DE_TU_REPO>
cd vet
```

---

### 2. Backend (Flask)

Sigue las instrucciones detalladas en [`app/README.md`](app/README.md), pero en resumen:

```sh
cd app
python -m venv .venv
.venv\Scripts\activate   # En Windows
pip install -r requirements.txt
# Configura tu base de datos en config.py o variables de entorno
python main.py
```
```sh
pip install cryptography
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
---

### 3. Frontend (Vue)

Sigue las instrucciones detalladas en [`frontend/README.md`](frontend/README.md), pero en resumen:

```sh
cd frontend
npm install
npm run dev
```

---

## Notas

- Consulta los README específicos en cada carpeta para detalles de configuración y uso.
- No subas archivos sensibles como `.env` o `instance/` a GitHub.
- Si usas migraciones en el backend, la carpeta `migrations/` debe estar incluida en el repositorio.

---
