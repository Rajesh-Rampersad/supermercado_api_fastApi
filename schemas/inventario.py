# app/esquemas/inventario.py

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

# ==========================================
# ESQUEMAS PARA CATEGORIA
# ==========================================

class CategoriaBase(BaseModel):
    nombre: str = Field(..., description="Nombre único de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción opcional")

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    
    # Pydantic v2: Configuración para leer atributos de modelos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

# ==========================================
# ESQUEMAS PARA PRODUCTO
# ==========================================

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del producto")
    precio: float = Field(..., gt=0, description="Precio del producto (debe ser mayor a 0)")
    cantidad: int = Field(..., ge=0, description="Cantidad en stock (no puede ser negativa)")
    categoria_id: int = Field(..., description="ID de la categoría a la que pertenece")

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True) # Permite leer datos de SQLAlchemy

# ==========================================
# ESQUEMAS ANIDADOS (Para respuestas enriquecidas)
# ==========================================

class CategoriaConProductos(Categoria):
    """Devuelve la categoría con su lista de productos asociados."""
    productos: List[Producto] = []

class ProductoConCategoria(Producto):
    """Devuelve un producto junto con los datos de su categoría."""
    categoria: Categoria

# ==========================================
# ESQUEMAS PARA OPERACIONES
# ==========================================

class VentaProducto(BaseModel):
    cantidad: int = Field(..., gt=0, description="Cantidad a vender (debe ser mayor a 0)")
