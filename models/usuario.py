class Usuario:
    def __init__(self, nombre, email, rol, contraseña, activo=True):
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.contraseña = contraseña
        self.activo = activo