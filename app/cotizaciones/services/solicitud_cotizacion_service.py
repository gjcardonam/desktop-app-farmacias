from app.cotizaciones.models.solicitud_cotizacion import SolicitudCotizacion, SolicitudCotizacionDetalle
from app.cotizaciones.repository import solicitud_cotizacion_repository

def crear_solicitud_cotizacion(id_sucursal, id_usuario, items, observaciones=None):
    try:
        solicitud = SolicitudCotizacion.crear(id_sucursal, id_usuario, observaciones)
        solicitud_id = solicitud_cotizacion_repository.insertar_solicitud_cotizacion(solicitud)

        for item in items:
            detalle = SolicitudCotizacionDetalle.crear(
                item["id_producto"], item["cantidad"], item.get("observaciones")
            )
            solicitud_cotizacion_repository.insertar_detalle_solicitud(solicitud_id, detalle)

        return True, f"Solicitud de cotización creada con ID {solicitud_id}"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error al crear la solicitud: {str(e)}"

def enviar_solicitud_a_proveedores(solicitud_id, proveedores):
    try:
        for prov_id in proveedores:
            solicitud_cotizacion_repository.registrar_envio_proveedor(solicitud_id, prov_id)
        return True, f"Solicitud enviada a {len(proveedores)} proveedor(es)."
    except Exception as e:
        return False, f"Error al enviar la solicitud: {str(e)}"
    
def listar_solicitudes():
    """
    Obtiene todas las solicitudes de cotización con sus datos principales.
    """
    try:
        return solicitud_cotizacion_repository.obtener_solicitudes()
    except Exception as e:
        return []