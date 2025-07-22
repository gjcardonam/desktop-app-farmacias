from db.connection import DBConnection

def buscar_productos_por_nombre(nombre):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio_venta, p.stock, f.nombre
        FROM Producto p
        JOIN Farmacia f ON f.id_farmacia = p.id_farmacia
        WHERE LOWER(p.nombre) LIKE LOWER(%s)
    """, (f"%{nombre}%",))
    rows = cur.fetchall()
    cur.close()

    return [{
        "id": r[0],
        "nombre": r[1],
        "descripcion": r[2],
        "precio_venta": r[3],
        "stock": r[4],
        "farmacia": r[5]
    } for r in rows]

def obtener_producto(producto_id):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio_venta, p.costo, p.stock, f.id_farmacia, f.nombre
        FROM Producto p
        JOIN Farmacia f ON f.id_farmacia = p.id_farmacia
        WHERE p.id_producto = %s
    """, (producto_id,))
    row = cur.fetchone()
    cur.close()
    
    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "precio_venta": row[3],
            "costo": row[4],
            "stock": row[5],
            "id_farmacia": row[6],
            "farmacia": row[7]
        }
    return None

def actualizar_producto_db(producto_id, producto):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Producto
        SET nombre = %s,
            descripcion = %s,
            precio_venta = %s,
            costo = %s,
            stock = %s,
            id_farmacia = %s
        WHERE id_producto = %s
    """, (
        producto.nombre,
        producto.descripcion,
        producto.precio_venta,
        producto.costo,
        producto.stock,
        producto.id_farmacia,
        producto_id
    ))
    conn.commit()
    cur.close()
    
    
def obtener_productos():
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio_venta, p.stock, f.nombre
        FROM Producto p
        JOIN Farmacia f ON f.id_farmacia = p.id_farmacia
    """)
    rows = cur.fetchall()
    cur.close()
    
    return [{
        "id": r[0],
        "nombre": r[1],
        "descripcion": r[2],
        "precio_venta": r[3],
        "stock": r[4],
        "farmacia": r[5]
    } for r in rows]

def insertar_producto(producto):
    conn = DBConnection.get_instance().get_connection()
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
    
def eliminar_producto(producto_id):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Producto
        WHERE id_producto = %s
    """, (producto_id,))
    conn.commit()
    cur.close()