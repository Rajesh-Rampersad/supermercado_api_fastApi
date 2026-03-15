# /home/rajesh/Documents/supermercado_api/app/routers/productos.py
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from modelos.inventario import Producto, Categoria
from schemas.inventario import ProductoCreate, ProductoConCategoria

# Configuración del router
router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

# Inyección de Dependencias (Antigravity Rule)
DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=ProductoConCategoria, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: DbSession):
    """
    Crea un nuevo producto en el sistema.
    Valida que la categoría asociada exista antes de la creación.
    """
    # Validación de negocio: Asegurar que la categoría existe
    categoria_db = db.query(Categoria).filter(Categoria.id == producto.categoria_id).first()
    if not categoria_db:
        raise HTTPException(status_code=404, detail=f"La categoría con id {producto.categoria_id} no fue encontrada")

    nuevo_producto = Producto(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


@router.get("/", response_model=List[ProductoConCategoria])
def obtener_productos(db: DbSession, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista paginada de productos, incluyendo la información de su categoría.
    Utiliza joinedload para evitar el problema N+1.
    """
    productos = db.query(Producto).options(joinedload(Producto.categoria)).offset(skip).limit(limit).all()
    return productos


@router.get("/{producto_id}", response_model=ProductoConCategoria)
def obtener_producto(producto_id: int, db: DbSession):
    """Obtiene un producto específico por su ID, incluyendo la información de su categoría."""
    producto = db.query(Producto).options(joinedload(Producto.categoria)).filter(Producto.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto