from db.connection import DBConnection

def obtener_farmacia(farmacia_id):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_farmacia, nombre, nit, direccion, telefono FROM Farmacia WHERE id_farmacia = %s", (farmacia_id,))
    row = cur.fetchone()
    cur.close()
    
    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "nit": row[2],
            "direccion": row[3],
            "telefono": row[4]
        }
    return None

def actualizar_farmacia_db(farmacia_id, farmacia):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Farmacia
        SET nombre = %s, nit = %s, direccion = %s, telefono = %s
        WHERE id_farmacia = %s
    """, (farmacia.nombre, farmacia.nit, farmacia.direccion, farmacia.telefono, farmacia_id))
    conn.commit()
    cur.close()
    

def obtener_farmacias():
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_farmacia, nombre, nit, direccion, telefono FROM Farmacia")
    rows = cur.fetchall()
    cur.close()
    
    return [{"id": r[0], "nombre": r[1], "nit": r[2], "direccion": r[3], "telefono": r[4]} for r in rows]

def insertar_farmacia(farmacia):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Farmacia (nombre, nit, direccion, telefono)
        VALUES (%s, %s, %s, %s)
    """, (farmacia.nombre, farmacia.nit, farmacia.direccion, farmacia.telefono))
    conn.commit()
    cur.close()
    