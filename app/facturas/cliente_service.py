from app.clientes.repository.cliente_repository import insertar_cliente
from app.clientes.models.cliente import Cliente
from app.clientes.repository.cliente_repository import obtener_clientes
from app.clientes.repository.cliente_repository import obtener_cliente, actualizar_cliente_db
from app.clientes.models.cliente import Cliente

def obtener_cliente_por_id(cliente_id):
    return obtener_cliente(cliente_id)
    
def actualizar_cliente(cliente_id, nombre, documento, telefono):
    try:
        cliente = Cliente.crear(nombre, documento, telefono)
        actualizar_cliente_db(cliente_id, cliente)
        return True, "Cliente actualizado correctamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, str(e)

def obtener_todos_los_clientes():
    return obtener_clientes()
    
def procesar_nuevo_cliente(nombre, documento, telefono):
    try:
        cliente = Cliente.crear(nombre, documento, telefono)
        insertar_cliente(cliente)
        return True, "Cliente guardado exitosamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, str(e)