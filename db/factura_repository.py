from db.connection import get_connection
from datetime import datetime

def insertar_factura_venta(id_cliente, productos):
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
    """, (datetime.now(), id_cliente, 1, total, "Pagada"))
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