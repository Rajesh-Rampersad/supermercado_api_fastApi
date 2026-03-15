# app/utils/security.py
from passlib.context import CryptContext

# Configuramos el algoritmo de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_password_hash(password: str) -> str:
    """Convierte texto plano en un hash seguro."""
    return pwd_context.hash(password)

def verificar_password(password_plana: str, password_hasheada: str) -> bool:
    """Compara una contraseña ingresada con el hash guardado."""
    return pwd_context.verify(password_plana, password_hasheada)