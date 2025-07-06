class Cliente:
    def __init__(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    @classmethod
    def crear(cls, nombre, documento, telefono):
        if not nombre or not documento:
            raise ValueError("Nombre y documento son obligatorios")
        # Se podrían agregar más validaciones aquí
        return cls(nombre.strip(), documento.strip(), telefono.strip() if telefono else "")