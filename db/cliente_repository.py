from db.connection import get_connection
from db.connection import get_connection

def obtener_cliente(cliente_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente, nombre, documento, telefono FROM Cliente WHERE id_cliente = %s", (cliente_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "documento": row[2],
            "telefono": row[3]
        }
    return None

def actualizar_cliente_db(cliente_id, cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Cliente
        SET nombre = %s, documento = %s, telefono = %s
        WHERE id_cliente = %s
    """, (cliente.nombre, cliente.documento, cliente.telefono, cliente_id))
    conn.commit()
    cur.close()
    conn.close()

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