from db.farmacia_repository import insertar_farmacia
from models.farmacia import Farmacia
from db.farmacia_repository import obtener_farmacias

def obtener_todas_las_farmacias():
    return obtener_farmacias()

def procesar_nueva_farmacia(nombre, nit, direccion, telefono):
    if not nombre or not nit:
        return False, "Nombre y NIT son obligatorios"
    
    farmacia = Farmacia(nombre, nit, direccion, telefono)
    
    try:
        insertar_farmacia(farmacia)
        return True, "Farmacia registrada correctamente"
    except Exception as e:
        return False, str(e)