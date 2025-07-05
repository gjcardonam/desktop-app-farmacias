from db.cliente_repository import insertar_cliente
from models.cliente import Cliente
from db.cliente_repository import obtener_clientes
from db.cliente_repository import obtener_cliente, actualizar_cliente_db
from models.cliente import Cliente

def obtener_cliente_por_id(cliente_id):
    return obtener_cliente(cliente_id)

def actualizar_cliente(cliente_id, nombre, documento, telefono):
    if not nombre or not documento:
        return False, "Nombre y documento son obligatorios"
    cliente = Cliente(nombre, documento, telefono)
    try:
        actualizar_cliente_db(cliente_id, cliente)
        return True, "Cliente actualizado correctamente"
    except Exception as e:
        return False, str(e)

def obtener_todos_los_clientes():
    return obtener_clientes()

def procesar_nuevo_cliente(nombre, documento, telefono):
    if not nombre or not documento:
        return False, "Nombre y documento son obligatorios"
    cliente = Cliente(nombre, documento, telefono)
    try:
        insertar_cliente(cliente)
        return True, "Cliente guardado exitosamente"
    except Exception as e:
        return False, str(e)