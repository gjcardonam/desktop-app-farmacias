from app.usuarios.repository.usuario_repository import buscar_usuario_por_credenciales

def autenticar_usuario(email, password):
    return buscar_usuario_por_credenciales(email, password)