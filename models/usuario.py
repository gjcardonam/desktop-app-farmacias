class Usuario:
    def __init__(self, nombre, email, rol, contraseña, activo=True):
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.contraseña = contraseña
        self.activo = activo

    @classmethod
    def crear(cls, nombre, email, rol, contraseña, activo=True):
        if not nombre or not email or not rol or not contraseña:
            raise ValueError("Todos los campos son obligatorios")
        if "@" not in email:
            raise ValueError("El correo electrónico no es válido")
        return cls(nombre.strip(), email.strip(), rol.strip(), contraseña.strip(), activo)