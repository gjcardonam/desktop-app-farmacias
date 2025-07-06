# services/factura_service.py

from app.facturas.repository.factura_repository import (
    insertar_factura_venta,
    obtener_todas_las_facturas,
    obtener_detalle_factura as repo_detalle_factura
)
from global_state import get_usuario
from app.facturas.models.factura import Factura

def obtener_detalle_factura(factura_id):
    """
    Retorna el detalle de una factura dado su ID.
    """
    return repo_detalle_factura(factura_id)

def registrar_factura(id_cliente, productos):
    """
    Registra una factura nueva validando los datos con el modelo.
    Devuelve (True, {"factura_id": id, "total": total}) en caso de éxito.
    Devuelve (False, mensaje) si ocurre algún error.
    """
    try:
        usuario = get_usuario()
        if not usuario or "id" not in usuario:
            return False, "Usuario no autenticado"

        factura = Factura.crear(id_cliente, productos, usuario["id"])
        factura_id, _ = insertar_factura_venta(
            factura.id_cliente, factura.productos, factura.id_usuario
        )
        return True, {"factura_id": factura_id, "total": factura.total}

    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error al registrar factura: {str(e)}"

def obtener_facturas():
    """
    Retorna una lista de todas las facturas registradas.
    """
    return obtener_todas_las_facturas()