# Veterinaria Frontend (Vue 3 + Vite)

Este es el frontend de la aplicación de gestión veterinaria, desarrollado con Vue 3 y Vite.

## Estructura del Proyecto

```
frontend/
├── public/                # Archivos públicos y estáticos
├── src/
│   ├── assets/            # Imágenes y recursos
│   ├── components/        # Componentes Vue reutilizables
│   ├── views/             # Vistas principales de la app
│   ├── App.vue            # Componente raíz
│   ├── main.js            # Punto de entrada de la app
│   ├── router.js          # Configuración de rutas
│   ├── axios.js           # Configuración de Axios
│   └── style.css          # Estilos globales
├── .vscode/               # Configuración recomendada de VS Code
├── .gitignore             # Archivos y carpetas a ignorar en Git
├── index.html             # HTML principal
├── package.json           # Dependencias y scripts de npm
├── README.md              # Este archivo
└── vite.config.js         # Configuración de Vite
```

## Requisitos

- Node.js 18+
- npm 9+ o yarn



2. **Instala las dependencias:**
   ```sh
   npm install
   # o
   yarn install
   ```

3. **Configura las variables de entorno (opcional):**
   - Si necesitas variables de entorno, crea un archivo `.env` en la raíz del frontend.
   - Ejemplo de variable para la URL base de la API:
     ```
     VITE_API_URL=http://localhost:5000
     ```

4. **Inicia la aplicación en modo desarrollo:**
   ```sh
   npm run dev
   # o
   yarn dev
   ```

   La app estará disponible en [http://localhost:5173](http://localhost:5173) por defecto.

## Proxy de API

El archivo [`vite.config.js`](vite.config.js) ya está configurado para redirigir las peticiones `/api` al backend Flask en `http://localhost:5000`.

## ¿Qué archivos subir a GitHub?

Debes subir todo el código fuente y archivos de configuración, excepto:

- `node_modules/`
- `dist/` (build de producción)
- Archivos de entorno `.env`
- Archivos temporales del sistema operativo y del editor

Tu archivo `.gitignore` ya está configurado para esto.

## Licencia

MIT License.