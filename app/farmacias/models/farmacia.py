class Farmacia:
    def __init__(self, nombre, nit, direccion, telefono):
        self.nombre = nombre
        self.nit = nit
        self.direccion = direccion
        self.telefono = telefono

    @classmethod
    def crear(cls, nombre, nit, direccion, telefono):
        if not nombre or not nit:
            raise ValueError("El nombre y el NIT son obligatorios")
        return cls(nombre.strip(), nit.strip(), direccion.strip() if direccion else "", telefono.strip() if telefono else "")