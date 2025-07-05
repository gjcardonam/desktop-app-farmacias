from db.connection import get_connection
from datetime import datetime

def obtener_detalle_factura(factura_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.nombre, dv.cantidad, dv.precio_unit, dv.impuesto
        FROM DetalleVenta dv
        JOIN Producto p ON dv.id_producto = p.id_producto
        WHERE dv.id_factura = %s
    """, (factura_id,))
    
    detalles = []
    for nombre, cantidad, precio_unit, impuesto in cur.fetchall():
        detalles.append({
            "producto": nombre,
            "cantidad": cantidad,
            "precio_unit": precio_unit,
            "impuesto": impuesto
        })

    cur.close()
    conn.close()
    return detalles

def obtener_todas_las_facturas():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            f.id_factura, 
            f.fecha, 
            c.nombre AS cliente, 
            u.nombre AS usuario, 
            f.total, 
            f.estado
        FROM FacturaVenta f
        JOIN Cliente c ON f.id_cliente = c.id_cliente
        JOIN Usuario u ON f.id_usuario = u.id_usuario
        ORDER BY f.fecha DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "fecha": r[1].strftime("%Y-%m-%d %H:%M"),
            "cliente": r[2],
            "usuario": r[3],
            "total": f"${r[4]:,.2f}",
            "estado": r[5]
        } for r in rows
    ]

def insertar_factura_venta(id_cliente, productos, id_usuario):
    conn = get_connection()
    cur = conn.cursor()

    total = 0
    for p in productos:
        cur.execute("SELECT precio_venta, stock FROM Producto WHERE id_producto = %s", (p["producto_id"],))
        precio, stock = cur.fetchone()
        if p["cantidad"] > stock:
            raise Exception(f"Stock insuficiente para producto ID {p['producto_id']}")
        total += precio * p["cantidad"]

    cur.execute("""
        INSERT INTO FacturaVenta (fecha, id_cliente, id_usuario, total, estado)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_factura    
    """, (datetime.now(), id_cliente, id_usuario, total, "Pagada"))
    factura_id = cur.fetchone()[0]

    for p in productos:
        cur.execute("SELECT precio_venta FROM Producto WHERE id_producto = %s", (p["producto_id"],))
        precio_unit = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO DetalleVenta (id_factura, id_producto, cantidad, precio_unit, impuesto)
            VALUES (%s, %s, %s, %s, %s)
        """, (factura_id, p["producto_id"], p["cantidad"], precio_unit, 0))
        cur.execute("""
            UPDATE Producto SET stock = stock - %s WHERE id_producto = %s
        """, (p["cantidad"], p["producto_id"]))

    conn.commit()
    cur.close()
    conn.close()
    return factura_id, total