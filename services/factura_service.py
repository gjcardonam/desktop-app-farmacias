from db.factura_repository import insertar_factura_venta
from global_state import get_usuario
from db.factura_repository import obtener_todas_las_facturas
from db.factura_repository import obtener_detalle_factura as repo_detalle_factura

def obtener_detalle_factura(factura_id):
    return repo_detalle_factura(factura_id)
    
def registrar_factura(id_cliente, productos):
    try:
        usuario = get_usuario()
        if not usuario:
            raise Exception("Usuario no autenticado")

        id_usuario = usuario["id"]

        factura_id, total = insertar_factura_venta(id_cliente, productos, id_usuario)
        return True, {"factura_id": factura_id, "total": total}
    except Exception as e:
        return False, str(e)
        

def obtener_facturas():
    return obtener_todas_las_facturas()