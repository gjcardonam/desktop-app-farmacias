from db.connection import get_connection

def obtener_clientes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente, nombre, documento, telefono FROM Cliente")
    clientes = [{"id": row[0], "nombre": row[1], "documento": row[2], "telefono": row[3]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return clientes

def insertar_cliente(cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Cliente (nombre, documento, telefono) VALUES (%s, %s, %s)",
        (cliente.nombre, cliente.documento, cliente.telefono)
    )
    conn.commit()
    cur.close()
    conn.close()