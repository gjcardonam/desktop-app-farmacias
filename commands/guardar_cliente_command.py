# commands/guardar_cliente_command.py

from services.cliente_service import procesar_nuevo_cliente

class GuardarClienteCommand:
    def __init__(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    def ejecutar(self):
        return procesar_nuevo_cliente(self.nombre, self.documento, self.telefono)