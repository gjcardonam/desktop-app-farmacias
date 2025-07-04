from db.producto_repository import insertar_producto
from models.producto import Producto
from db.producto_repository import obtener_productos

def obtener_todos_los_productos():
    return obtener_productos()

def procesar_nuevo_producto(nombre, descripcion, precio, costo, stock, id_farmacia):
    if not nombre or precio <= 0 or costo < 0 or stock < 0:
        return False, "Datos inválidos: revisa nombre, precio, costo o stock"

    producto = Producto(nombre, descripcion, precio, costo, stock, id_farmacia)
    try:
        insertar_producto(producto)
        return True, "Producto registrado correctamente"
    except Exception as e:
        return False, str(e)