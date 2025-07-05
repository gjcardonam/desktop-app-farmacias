from db.producto_repository import insertar_producto
from models.producto import Producto
from db.producto_repository import obtener_productos
from db.producto_repository import obtener_producto, actualizar_producto_db
from models.producto import Producto

def obtener_producto_por_id(producto_id):
    return obtener_producto(producto_id)

def actualizar_producto(producto_id, nombre, descripcion, precio, costo, stock, id_farmacia):
    if not nombre or precio <= 0 or costo < 0 or stock < 0:
        return False, "Datos inválidos"
    producto = Producto(nombre, descripcion, precio, costo, stock, id_farmacia)
    try:
        actualizar_producto_db(producto_id, producto)
        return True, "Producto actualizado correctamente"
    except Exception as e:
        return False, str(e)
    
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