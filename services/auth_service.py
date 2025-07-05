from db.connection import get_connection

def autenticar_usuario(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_usuario, nombre, email, rol
        FROM Usuario
        WHERE email = %s AND contraseña = %s AND activo = TRUE
    """, (email, password))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "email": row[2],
            "rol": row[3]
        }
    return None