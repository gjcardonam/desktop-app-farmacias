from services.cliente_service import procesar_nuevo_cliente

def guardar_cliente(nombre, documento, telefono):
    return procesar_nuevo_cliente(nombre, documento, telefono)