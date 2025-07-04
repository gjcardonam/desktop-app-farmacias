from services.farmacia_service import procesar_nueva_farmacia

def guardar_farmacia(nombre, nit, direccion, telefono):
    return procesar_nueva_farmacia(nombre, nit, direccion, telefono)