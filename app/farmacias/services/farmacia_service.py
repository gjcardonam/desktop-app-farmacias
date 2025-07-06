# services/farmacia_service.py

from app.farmacias.repository.farmacia_repository import (
    insertar_farmacia,
    obtener_farmacias,
    obtener_farmacia,
    actualizar_farmacia_db
)
from app.farmacias.models.farmacia import Farmacia

def obtener_farmacia_por_id(farmacia_id):
    """
    Retorna una farmacia por su ID.
    """
    return obtener_farmacia(farmacia_id)

def actualizar_farmacia(farmacia_id, nombre, nit, direccion, telefono):
    """
    Actualiza una farmacia existente con validación de datos.
    """
    try:
        farmacia = Farmacia.crear(nombre, nit, direccion, telefono)
        actualizar_farmacia_db(farmacia_id, farmacia)
        return True, "Farmacia actualizada correctamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error al actualizar farmacia: {str(e)}"

def obtener_todas_las_farmacias():
    """
    Retorna todas las farmacias almacenadas.
    """
    return obtener_farmacias()

def procesar_nueva_farmacia(nombre, nit, direccion, telefono):
    """
    Procesa el registro de una nueva farmacia con validaciones.
    """
    try:
        farmacia = Farmacia.crear(nombre, nit, direccion, telefono)
        insertar_farmacia(farmacia)
        return True, "Farmacia registrada correctamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error al registrar farmacia: {str(e)}"