from db.connection import DBConnection

def insertar_solicitud_cotizacion(solicitud):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO SolicitudCotizacion (id_sucursal, id_usuario, observaciones, estado)
        VALUES (%s, %s, %s, %s)
        RETURNING id_solicitud
    """, (solicitud.id_sucursal, solicitud.id_usuario, solicitud.observaciones, solicitud.estado))
    solicitud_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return solicitud_id

def insertar_detalle_solicitud(solicitud_id, detalle):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO SolicitudCotizacionDetalle (id_solicitud, id_producto, cantidad, observaciones)
        VALUES (%s, %s, %s, %s)
    """, (solicitud_id, detalle.id_producto, detalle.cantidad, detalle.observaciones))
    conn.commit()
    cur.close()

def registrar_envio_proveedor(solicitud_id, proveedor_id):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO SolicitudCotizacionProveedor (id_solicitud, id_proveedor)
        VALUES (%s, %s)
    """, (solicitud_id, proveedor_id))
    conn.commit()
    cur.close()

def obtener_solicitudes():
    """
    Devuelve todas las solicitudes de cotización con sus datos principales.
    """
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_solicitud, fecha_creacion, estado, observaciones
        FROM SolicitudCotizacion
        ORDER BY fecha_creacion DESC
    """)
    rows = cur.fetchall()
    cur.close()

    return [
        {
            "id": row[0],
            "fecha_creacion": row[1],
            "estado": row[2],
            "observaciones": row[3]
        }
        for row in rows
    ]