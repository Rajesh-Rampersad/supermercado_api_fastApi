# app/modelos/inventario.py
# Los modelos representan las tablas en tu base de datos SQLite. Vamos a crear la relación entre Categorías y Productos.

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Se puede definir un modelo para las categorías de los productos
class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String, nullable=True)

    # Esta relación crea un atributo 'productos' en las instancias de Categoria
    # que contiene una lista de los productos asociados.
    productos = relationship("Producto", back_populates="categoria")

# El modelo principal podría ser Producto, que contiene la información del inventario
class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    cantidad = Column(Integer) # La cantidad en stock es parte del inventario

    # Aquí se usa ForeignKey para establecer la relación con la tabla 'categorias'.
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="productos")
