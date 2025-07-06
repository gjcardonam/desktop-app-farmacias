# services/producto_service.py

from app.productos.repository.producto_repository import (
    insertar_producto,
    obtener_productos,
    obtener_producto,
    actualizar_producto_db,
    buscar_productos_por_nombre
)
from app.productos.models.producto import Producto

def buscar_productos(nombre):
    return buscar_productos_por_nombre(nombre)

def obtener_producto_por_id(producto_id):
    """
    Retorna un producto por su ID.
    """
    return obtener_producto(producto_id)

def actualizar_producto(producto_id, nombre, descripcion, precio, costo, stock, id_farmacia):
    """
    Actualiza un producto existente usando el Factory Method.
    """
    try:
        producto = Producto.crear(nombre, descripcion, precio, costo, stock, id_farmacia)
        actualizar_producto_db(producto_id, producto)
        return True, "Producto actualizado correctamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error al actualizar producto: {str(e)}"

def obtener_todos_los_productos():
    """
    Retorna todos los productos almacenados.
    """
    return obtener_productos()

def procesar_nuevo_producto(nombre, descripcion, precio, costo, stock, id_farmacia):
    """
    Registra un nuevo producto validando todos los campos.
    """
    try:
        producto = Producto.crear(nombre, descripcion, precio, costo, stock, id_farmacia)
        insertar_producto(producto)
        return True, "Producto registrado correctamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error al registrar producto: {str(e)}"