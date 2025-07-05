# services/usuario_service.py

from db.usuario_repository import (
    insertar_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario_db
)
from models.usuario import Usuario

def procesar_nuevo_usuario(nombre, email, rol, contraseña):
    """
    Crea un nuevo usuario con validación integrada usando el Factory Method.
    """
    try:
        usuario = Usuario.crear(nombre, email, rol, contraseña)
        insertar_usuario(usuario)
        return True, "Usuario registrado correctamente"
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"Error al registrar usuario: {str(e)}"

def obtener_todos_los_usuarios():
    """
    Retorna todos los usuarios.
    """
    return obtener_usuarios()

def obtener_usuario(id_usuario):
    """
    Retorna un usuario por ID.
    """
    return obtener_usuario_por_id(id_usuario)

def procesar_actualizacion_usuario(id_usuario, nombre, email, rol, activo, nueva_contraseña=None):
    """
    Actualiza un usuario existente, validando los campos obligatorios.
    """
    if not nombre or not email or not rol:
        return False, "Nombre, correo y rol son obligatorios"
    
    if "@" not in email:
        return False, "Correo electrónico no válido"

    try:
        # Como no se actualiza el objeto completo, no usamos `Usuario.crear`
        actualizar_usuario_db(id_usuario, nombre.strip(), email.strip(), rol.strip(), activo, nueva_contraseña.strip() if nueva_contraseña else None)
        return True, "Usuario actualizado correctamente"
    except Exception as e:
        return False, f"Error al actualizar usuario: {str(e)}"