from db.connection import get_connection

def obtener_farmacias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_farmacia, nombre, nit, direccion, telefono FROM Farmacia")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "nit": r[2], "direccion": r[3], "telefono": r[4]} for r in rows]

def insertar_farmacia(farmacia):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Farmacia (nombre, nit, direccion, telefono)
        VALUES (%s, %s, %s, %s)
    """, (farmacia.nombre, farmacia.nit, farmacia.direccion, farmacia.telefono))
    conn.commit()
    cur.close()
    conn.close()