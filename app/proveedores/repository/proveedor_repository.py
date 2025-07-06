from db.connection import DBConnection

def obtener_proveedor(proveedor_id):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_proveedor, nombre, documento, telefono, email
        FROM Proveedor
        WHERE id_proveedor = %s
    """, (proveedor_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "documento": row[2],
            "telefono": row[3],
            "email": row[4]
        }
    return None

def actualizar_proveedor_db(proveedor_id, proveedor):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Proveedor
        SET nombre = %s,
            documento = %s,
            telefono = %s,
            email = %s
        WHERE id_proveedor = %s
    """, (
        proveedor.nombre,
        proveedor.documento,
        proveedor.telefono,
        proveedor.email,
        proveedor_id
    ))
    conn.commit()
    cur.close()

def insertar_proveedor(proveedor):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Proveedor (nombre, documento, telefono, email)
        VALUES (%s, %s, %s, %s)
    """, (proveedor.nombre, proveedor.documento, proveedor.telefono, proveedor.email))
    conn.commit()
    cur.close()

def obtener_proveedores():
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_proveedor, nombre, documento, telefono, email FROM Proveedor")
    rows = cur.fetchall()
    cur.close()
    return [{
        "id": r[0],
        "nombre": r[1],
        "documento": r[2],
        "telefono": r[3],
        "email": r[4]
    } for r in rows]