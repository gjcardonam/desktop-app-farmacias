from app.proveedores.repository.proveedor_repository import insertar_proveedor, obtener_proveedores
from app.proveedores.models.proveedor import Proveedor
from app.proveedores.repository.proveedor_repository import actualizar_proveedor_db, obtener_proveedor

def actualizar_proveedor(proveedor_id, nombre, documento, telefono, email):
    try:
        proveedor = Proveedor.crear(nombre, documento, telefono, email)
        actualizar_proveedor_db(proveedor_id, proveedor)
        return True, "Proveedor actualizado correctamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error: {str(e)}"

def obtener_proveedor_por_id(proveedor_id):
    return obtener_proveedor(proveedor_id)

def procesar_nuevo_proveedor(nombre, documento, telefono, email):
    try:
        proveedor = Proveedor.crear(nombre, documento, telefono, email)
        insertar_proveedor(proveedor)
        return True, "Proveedor guardado exitosamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error: {str(e)}"

def obtener_todos_los_proveedores():
    return obtener_proveedores()