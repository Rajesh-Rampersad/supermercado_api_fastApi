# /home/rajesh/Documents/supermercado_api/app/main.py
from fastapi import FastAPI

# Importaciones de nuestros módulos
from app.database import Base, engine

# Aunque 'inventario' no se usa directamente aquí, esta importación es VITAL.
# Asegura que SQLAlchemy conozca nuestros modelos (Categoria, Producto)
# antes de que le pidamos que cree las tablas.
from modelos import inventario, usuarios
from routers import categorias, productos, usuarios

# --- Creación de Tablas en la Base de Datos ---
# Esta línea le dice a SQLAlchemy que revise todos los modelos que heredan de `Base`
# y cree las tablas correspondientes en la base de datos si aún no existen.
# Esto se ejecuta una sola vez cuando la aplicación se inicia.
Base.metadata.create_all(bind=engine)


# --- Instancia de la Aplicación FastAPI ---
# Aquí creamos la instancia principal de nuestra API.
# Los metadatos como title, description y version son importantes
# porque se mostrarán en la documentación automática (Swagger).
app = FastAPI(
    title="Supermercado API",
    description="Una API elegante y robusta para gestionar el inventario de un supermercado.",
    version="1.0.0",
    contact={
        "name": "L7 Fullstack Architect",
    },
)


# --- Registro de Enrutadores (Routers) ---
app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(usuarios.router)


# --- Endpoint Raíz (Health Check) ---
@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz para verificar que la API está funcionando correctamente.
    """
    return {"status": "ok", "message": "¡Bienvenido a la Supermercado API!"}
