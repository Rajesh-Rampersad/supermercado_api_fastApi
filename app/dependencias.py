# /home/rajesh/Documents/supermercado_api/app/dependencias.py
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verificar_api_key(api_key: str = Security(api_key_header)):
    """Verifica que el cliente proporcione la API Key correcta en la cabecera."""
    if api_key != settings.SECRET_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No autorizado. API Key inválida o faltante."
        )
    return api_key