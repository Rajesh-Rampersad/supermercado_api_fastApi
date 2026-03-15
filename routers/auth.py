#  app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from modelos.usuarios import Usuario
from schemas.usuarios import UsuarioCreate, UsuarioResponse
from app.utils.security import obtener_password_hash

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el usuario ya existe
    db_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="El email ya está registrado"
        )
    
    # 2. Hashear la contraseña (¡Regla de oro de seguridad!)
    hashed_pwd = obtener_password_hash(usuario.password)
    
    # 3. Crear instancia y guardar
    nuevo_usuario = Usuario(
        email=usuario.email,
        hashed_password=hashed_pwd,
        rol=usuario.rol
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario