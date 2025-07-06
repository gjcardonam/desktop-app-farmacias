class Proveedor:
    def __init__(self, nombre, documento, telefono, email):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono
        self.email = email

    @classmethod
    def crear(cls, nombre, documento, telefono, email):
        if not nombre or not documento:
            raise ValueError("El nombre y el documento son obligatorios")
        return cls(nombre, documento, telefono, email)