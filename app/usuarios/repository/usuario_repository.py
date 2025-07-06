from db.connection import DBConnection

def buscar_usuario_por_credenciales(email, password):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_usuario, nombre, email, rol
        FROM Usuario
        WHERE email = %s AND contraseña = %s AND activo = TRUE
    """, (email, password))
    row = cur.fetchone()
    cur.close()

    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "email": row[2],
            "rol": row[3]
        }
    return None

def insertar_usuario(usuario):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Usuario (nombre, email, rol, contraseña, activo)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        usuario.nombre,
        usuario.email,
        usuario.rol,
        usuario.contraseña,
        usuario.activo
    ))
    conn.commit()
    cur.close()
    

def obtener_usuarios():
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nombre, email, rol, activo FROM Usuario")
    rows = cur.fetchall()
    cur.close()
    
    return [
        {
            "id": r[0],
            "nombre": r[1],
            "email": r[2],
            "rol": r[3],
            "activo": r[4]
        }
        for r in rows
    ]

def obtener_usuario_por_id(id_usuario):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_usuario, nombre, email, rol, activo
        FROM Usuario
        WHERE id_usuario = %s
    """, (id_usuario,))
    row = cur.fetchone()
    cur.close()
    
    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "email": row[2],
            "rol": row[3],
            "activo": row[4]
        }
    return None

def actualizar_usuario_db(id_usuario, nombre, email, rol, activo, nueva_contraseña=None):
    conn = DBConnection.get_instance().get_connection()
    cur = conn.cursor()

    if nueva_contraseña:
        cur.execute("""
            UPDATE Usuario
            SET nombre = %s,
                email = %s,
                rol = %s,
                activo = %s,
                contraseña = %s
            WHERE id_usuario = %s
        """, (nombre, email, rol, activo, nueva_contraseña, id_usuario))
    else:
        cur.execute("""
            UPDATE Usuario
            SET nombre = %s,
                email = %s,
                rol = %s,
                activo = %s
            WHERE id_usuario = %s
        """, (nombre, email, rol, activo, id_usuario))

    conn.commit()
    cur.close()
    