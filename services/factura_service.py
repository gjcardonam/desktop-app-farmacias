from db.factura_repository import insertar_factura_venta
from global_state import get_usuario
    
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