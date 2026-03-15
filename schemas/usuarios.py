# /home/rajesh/Documents/supermercado_api/schemas/usuarios.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from modelos.usuarios import UserRole

class UsuarioBase(BaseModel):
    email: EmailStr = Field(...)
    rol: UserRole = Field(default=UserRole.CLIENTE) # Swagger mostrará opciones fijas

class UsuarioCreate(UsuarioBase):
    # En la creación recibimos la contraseña plana, pero NUNCA la devolvemos
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def validar_password(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not any(char.isdigit() for char in v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

class UsuarioResponse(UsuarioBase):
    # En la respuesta devolvemos el ID, pero excluimos la contraseña (incluso el hash)
    id: int

    # Pydantic v2: Configuración para leer atributos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)