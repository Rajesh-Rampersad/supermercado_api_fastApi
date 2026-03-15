# app/modelos/usuarios.py
from sqlalchemy import Column, Integer, String, Enum
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CAJERO = "cajero"
    CLIENTE = "cliente"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rol = Column(String, default=UserRole.CLIENTE) # Guardamos el rol como string