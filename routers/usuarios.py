# /home/rajesh/Documents/supermercado_api/app/routers/usuarios.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.security import obtener_password_hash
from modelos.usuarios import Usuario
from schemas.usuarios import UsuarioCreate, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

DbSession = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: DbSession):
    """Registra un nuevo usuario asegurando su contraseña."""
    # Validación de negocio: El email no debe existir previamente
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Hashear la contraseña antes de guardarla (¡NUNCA GUARDAR EN TEXTO PLANO!)
    usuario_dict = usuario.model_dump()
    password_plana = usuario_dict.pop("password")
    
    nuevo_usuario = Usuario(**usuario_dict, hashed_password=obtener_password_hash(password_plana))
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario