
# 🛒 Supermercado API - Documentación Visual

## 📊 1. Modelo de Datos (ERD)

Representación de las tablas y sus relaciones en el sistema de inventario.

```mermaid
erDiagram
    CATEGORIAS ||--o{ PRODUCTOS : "contiene"
    USUARIOS ||--o{ ORDENES : "realiza"

    CATEGORIAS {
        int id PK
        string nombre UK "unique, index"
        string descripcion "nullable"
    }

    PRODUCTOS {
        int id PK
        string nombre "index"
        float precio
        int cantidad
        int categoria_id FK
    }

    USUARIOS {
        int id PK
        string email UK
        string hashed_password
        string rol "admin | cajero | cliente"
    }

```

---

## 🔄 2. Flujos de Secuencia de Inventario

Procesos básicos de validación y reglas de negocio.

### A. Registro de Productos y Categorías

```mermaid
sequenceDiagram
    autonumber
    actor Client as Cliente
    participant Router as Router (FastAPI)
    participant Schema as Pydantic (Schemas)
    participant DB as SQLAlchemy (Session)

    Client->>Router: POST /productos/ {datos}
    Router->>Schema: Valida Request
    
    alt Datos Válidos
        Router->>DB: Verifica Categoría
        Router->>DB: db.add() & db.commit()
        Router-->>Client: 201 Created
    else Datos Inválidos
        Schema-->>Client: 422 Unprocessable Entity
    end

```

### B. Venta de Productos (Gestión de Stock)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Cliente
    participant Router as Router (FastAPI)
    participant DB as SQLAlchemy (Session)

    Client->>Router: POST /productos/{id}/vender {cantidad}
    Router->>DB: Consulta Producto
    
    alt Stock insuficiente
        Router-->>Client: 400 Bad Request
    else Stock suficiente
        Router->>DB: Actualiza cantidad y commit()
        Router-->>Client: 200 OK
    end

```

---

## 🔐 3. Seguridad Avanzada (Auth & RBAC)

Flujo de acceso basado en tokens JWT y permisos por rol.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Cliente
    participant Auth as Auth Router (/token)
    participant Security as Dependencias (JWT/RBAC)
    participant Router as API Router
    participant DB as Base de Datos

    Note over Client, DB: 🔑 Flujo de Login y Generación de JWT
    Client->>Auth: POST /token (email, password)
    Auth->>DB: Busca Usuario por email
    DB-->>Auth: Instancia de Usuario (con hashed_password)
    Auth->>Auth: Verifica password plana vs hash (Passlib)
    Auth-->>Client: Retorna JWT Access Token

    Note over Client, DB: 🛡️ Petición Protegida con Roles (ej. DELETE /productos)
    Client->>Router: DELETE /productos/1 (Header: Authorization Bearer)
    Router->>Security: validar_token_y_rol(rol_requerido="admin")
    Security->>Security: Decodifica y verifica firma del JWT
    Security->>DB: Obtiene Usuario desde payload del Token
    DB-->>Security: Objeto Usuario actual
    
    alt Usuario.rol != "admin"
        Security-->>Client: 403 Forbidden (Permisos insuficientes)
    else Usuario.rol == "admin"
        Security-->>Router: Permite acceso (Inyecta el usuario actual)
        Router->>DB: db.delete() y db.commit()
        Router-->>Client: 204 No Content
    end

```

