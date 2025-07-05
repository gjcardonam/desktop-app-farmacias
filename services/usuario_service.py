from db.usuario_repository import (
    insertar_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario_db
)
from models.usuario import Usuario

def procesar_nuevo_usuario(nombre, email, rol, contraseña):
    if not nombre or not email or not rol or not contraseña:
        return False, "Todos los campos son obligatorios"
    
    usuario = Usuario(nombre, email, rol, contraseña)
    try:
        insertar_usuario(usuario)
        return True, "Usuario registrado correctamente"
    except Exception as e:
        return False, str(e)

def obtener_todos_los_usuarios():
    return obtener_usuarios()

def obtener_usuario(id_usuario):
    return obtener_usuario_por_id(id_usuario)

def procesar_actualizacion_usuario(id_usuario, nombre, email, rol, activo, nueva_contraseña=None):
    if not nombre or not email or not rol:
        return False, "Todos los campos obligatorios deben estar completos"
    try:
        actualizar_usuario_db(id_usuario, nombre, email, rol, activo, nueva_contraseña)
        return True, "Usuario actualizado correctamente"
    except Exception as e:
        return False, str(e)