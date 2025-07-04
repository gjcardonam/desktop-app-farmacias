from db.connection import get_connection

def obtener_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_producto, p.nombre, p.precio_venta, p.stock, f.nombre
        FROM Producto p
        JOIN Farmacia f ON f.id_farmacia = p.id_farmacia
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{
        "id": r[0],
        "nombre": r[1],
        "precio_venta": r[2],
        "stock": r[3],
        "farmacia": r[4]
    } for r in rows]

def insertar_producto(producto):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Producto (nombre, descripcion, precio_venta, costo, stock, id_farmacia)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        producto.nombre,
        producto.descripcion,
        producto.precio_venta,
        producto.costo,
        producto.stock,
        producto.id_farmacia
    ))
    conn.commit()
    cur.close()
    conn.close()