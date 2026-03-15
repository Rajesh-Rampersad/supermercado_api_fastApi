# /home/rajesh/Documents/supermercado_api/app/routers/categorias.py
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from modelos.inventario import Categoria
from schemas.inventario import CategoriaCreate, Categoria as CategoriaSchema

# Configuración del router
router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)

# Inyección de Dependencias (Antigravity Rule)
DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=CategoriaSchema, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: CategoriaCreate, db: DbSession):
    """Crea una nueva categoría en el sistema."""
    # Verificar si la categoría ya existe para evitar duplicados
    db_categoria = db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first()
    if db_categoria:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    
    # Extraer los datos validados por Pydantic (model_dump en v2) y pasarlos a SQLAlchemy
    nueva_categoria = Categoria(**categoria.model_dump())
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria


@router.get("/", response_model=List[CategoriaSchema])
def obtener_categorias(db: DbSession, skip: int = 0, limit: int = 100):
    """Obtiene una lista paginada de categorías."""
    return db.query(Categoria).offset(skip).limit(limit).all()


@router.get("/{categoria_id}", response_model=CategoriaSchema)
def obtener_categoria(categoria_id: int, db: DbSession):
    """Obtiene una categoría específica por su ID."""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.put("/{categoria_id}", response_model=CategoriaSchema)
def actualizar_categoria(categoria_id: int, categoria_actualizada: CategoriaCreate, db: DbSession):
    """Actualiza los datos de una categoría existente."""
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    for key, value in categoria_actualizada.model_dump().items():
        setattr(db_categoria, key, value)
        
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: int, db: DbSession):
    """Elimina una categoría del sistema."""
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_categoria)
    db.commit()
