from db.factura_repository import insertar_factura_venta

def registrar_factura(id_cliente, productos):
    try:
        factura_id, total = insertar_factura_venta(id_cliente, productos)
        return True, {"factura_id": factura_id, "total": total}
    except Exception as e:
        return False, str(e)