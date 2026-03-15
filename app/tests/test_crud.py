# /home/rajesh/Documents/supermercado_api/tests/test_crud.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from app.main import app
from app.database import Base, get_db

# Usar SQLite en memoria para pruebas rápidas y aisladas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescribir la dependencia get_db para que use la BD de prueba
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture de Pytest para el cliente y la base de datos
@pytest.fixture(scope="module")
def client():
    # Arrange: Crear las tablas en la base de datos en memoria
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Cleanup: Limpiar las tablas después de las pruebas
    Base.metadata.drop_all(bind=engine)

# --- PRUEBAS PARA CATEGORÍAS ---

def test_crear_categoria(client):
    response = client.post(
        "/categorias/",
        json={"nombre": "Electrónica", "descripcion": "Gadgets"}
    )
    assert response.status_code == 201
    assert response.json()["nombre"] == "Electrónica"

def test_obtener_categorias(client):
    response = client.get("/categorias/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_actualizar_categoria(client):
    response = client.put(
        "/categorias/1",
        json={"nombre": "Hogar", "descripcion": "Cosas de casa"}
    )
    assert response.status_code == 200
    assert response.json()["nombre"] == "Hogar"

# --- PRUEBAS PARA PRODUCTOS ---

def test_crear_producto(client):
    response = client.post(
        "/productos/",
        json={"nombre": "Lámpara", "precio": 25.5, "cantidad": 10, "categoria_id": 1}
    )
    assert response.status_code == 201
    assert response.json()["nombre"] == "Lámpara"
    assert response.json()["categoria"]["nombre"] == "Hogar" # Verifica la relación Anidada

def test_obtener_productos_filtros(client):
    # Crear productos adicionales para la prueba de filtros
    client.post("/productos/", json={"nombre": "Silla", "precio": 15.0, "cantidad": 5, "categoria_id": 1})
    client.post("/productos/", json={"nombre": "Mesa", "precio": 45.0, "cantidad": 2, "categoria_id": 1})
    client.post("/productos/", json={"nombre": "Sillón", "precio": 60.0, "cantidad": 1, "categoria_id": 1})

    # Filtro por nombre (case-insensitive y parcial)
    response = client.get("/productos/?nombre=sill")
    assert response.status_code == 200
    nombres = [p["nombre"] for p in response.json()]
    assert "Silla" in nombres
    assert "Sillón" in nombres
    assert "Mesa" not in nombres

    # Filtro por rango de precios
    response = client.get("/productos/?precio_min=20&precio_max=50")
    assert response.status_code == 200
    nombres = [p["nombre"] for p in response.json()]
    assert "Mesa" in nombres # 45.0
    assert "Lámpara" in nombres # 25.5 (creada en test previo)
    assert "Silla" not in nombres # 15.0
    assert "Sillón" not in nombres # 60.0

def test_crear_producto_categoria_invalida(client):
    response = client.post(
        "/productos/",
        json={"nombre": "Error", "precio": 10, "cantidad": 1, "categoria_id": 999}
    )
    assert response.status_code == 404

def test_vender_producto_exito(client):
    response = client.post(
        "/productos/1/vender",
        json={"cantidad": 2}
    )
    assert response.status_code == 200
    assert response.json()["cantidad"] == 8

def test_vender_producto_stock_insuficiente(client):
    response = client.post(
        "/productos/1/vender",
        json={"cantidad": 100}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Stock insuficiente"

def test_eliminar_producto_sin_api_key(client):
    response = client.delete("/productos/1")
    assert response.status_code == 403

def test_eliminar_producto_con_api_key(client):
    response = client.delete("/productos/1", headers={"X-API-Key": "supersecreto123"})
    assert response.status_code == 204

def test_eliminar_categoria(client):
    response = client.delete("/categorias/1")
    assert response.status_code == 204