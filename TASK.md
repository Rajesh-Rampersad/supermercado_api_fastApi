# 📋 Flight Plan: Implementación de Endpoints CRUD

**1. Objective:**
Desarrollar los enrutadores (routers) y endpoints CRUD para gestionar `Categoria` y `Producto` en la API, conectando exitosamente la base de datos, los modelos SQLAlchemy y los esquemas Pydantic.

**2. Architecture Impact:**
- Creación de la capa de controladores (enrutadores) bajo el directorio `app/routers/`.
- Archivos nuevos: `app/routers/categorias.py` y `app/routers/productos.py`.
- Actualización de `app/main.py` para registrar los nuevos enrutadores mediante `app.include_router()`.

**3. Step-by-Step Checklist:**
- [x] Fase 1: Configurar Base de Datos (`app/database.py`).
- [x] Fase 2: Crear Modelos SQLAlchemy (`modelos/inventario.py`).
- [x] Fase 3: Crear Esquemas Pydantic (`schemas/inventario.py`).
- [x] Fase 4: Configurar Entrypoint y Swagger (`app/main.py`).
- [x] Fase 5: Implementar lógica CRUD para `Categoria` (GET, POST, GET/{id}, PUT, DELETE).
- [x] Fase 6: Implementar lógica CRUD para `Producto` (GET, POST, GET/{id}, PUT, DELETE).
- [x] Fase 7: Integrar los routers en `app/main.py`.
- [x] Fase 8: Pruebas unitarias/integración con Pytest.
  - [x] Configurar TestClient y BD en memoria (`sqlite:///:memory:`).
  - [x] Crear suite de pruebas para el ciclo de vida (CRUD) completo.
- [x] Fase 9: Generar Diagramas de Secuencia (Mermaid.js) para los flujos de petición.

**4. Verification:**
- Ejecutar la aplicación con Uvicorn y acceder a `http://127.0.0.1:8000/docs`.
- Poder crear (POST) una nueva categoría y un nuevo producto.
- Poder listar (GET) las categorías y productos creados, observando la persistencia en `supermercado.db`.

**Fase 10: Lógica de Venta y Seguridad**
- [x] Lógica de Stock: Crear endpoint POST `/productos/{id}/vender`.
- [x] Validación de Regla de Negocio: Stock insuficiente -> 400.
- [x] Seguridad Inicial: API Key en `dependencias.py` para DELETE `/productos/{id}`.

**Fase 11: Filtros Avanzados en Productos**
- [x] Actualizar endpoint `GET /productos/` para aceptar `nombre` (str), `precio_min` (float) y `precio_max` (float) como Query Parameters opcionales.
- [x] Modificar la consulta de SQLAlchemy para aplicar estos filtros de forma dinámica.
- [x] Agregar pruebas en `test_crud.py` para verificar que la búsqueda y los rangos de precios funcionan.

**Fase 12: Gestión de Variables de Entorno (Dotenv)**
- [x] Instalar `pydantic-settings` para manejo de configuración robusto y tipado.
- [x] Crear archivo `app/config.py` con una clase `Settings` para validar `DATABASE_URL` y `SECRET_API_KEY`.
- [x] Refactorizar `app/database.py` y `app/dependencias.py` para consumir la configuración de forma segura.
- [x] Crear archivo de plantilla `.env.example` para documentar los secretos requeridos.

**Fase 13: Modelo de Usuarios y Roles**
- [x] Crear modelo SQLAlchemy `Usuario` con campos `email`, `hashed_password` y `rol` (admin, cajero, cliente).
- [x] Crear esquemas Pydantic (`UsuarioCreate`, `UsuarioResponse`).
- [x] Crear endpoint `POST /usuarios/` para registrar nuevos usuarios (hasheando la contraseña con passlib).

**Fase 14: Autenticación con JWT**
- [ ] Instalar dependencias: `passlib[bcrypt]`, `python-jose[cryptography]`, `python-multipart`.
- [x] Refactorización: Crear `app/utils/security.py` para centralizar hashing y verificación de contraseñas.
- [ ] Configurar variables de entorno `JWT_SECRET_KEY` y `ALGORITHM` en `app/config.py`.
- [ ] Crear enrutador de autenticación y endpoint `POST /token` que valide credenciales y retorne un JWT.

**Fase 15: Autorización y RBAC (Role-Based Access Control)**
- [ ] Refactorizar `app/dependencias.py` con `OAuth2PasswordBearer` para extraer y validar el JWT.
- [ ] Crear dependencias de roles (ej. `requiere_admin`, `requiere_cajero_o_admin`).
- [ ] Proteger los endpoints de inventario reemplazando la antigua `API Key` por estas nuevas políticas.