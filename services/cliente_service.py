from db.cliente_repository import insertar_cliente
from models.cliente import Cliente
from db.cliente_repository import obtener_clientes

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