from datetime import datetime

class SolicitudCotizacion:
    def __init__(self, id_sucursal, id_usuario, observaciones=None, fecha_creacion=None, estado="Abierta"):
        self.id_sucursal = id_sucursal
        self.id_usuario = id_usuario
        self.observaciones = observaciones or ""
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.estado = estado

    @classmethod
    def crear(cls, id_sucursal, id_usuario, observaciones=None):
        if not id_sucursal or not id_usuario:
            raise ValueError("La sucursal y el usuario son obligatorios")
        return cls(id_sucursal, id_usuario, observaciones)

class SolicitudCotizacionDetalle:
    def __init__(self, id_producto, cantidad, observaciones=None):
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.observaciones = observaciones or ""

    @classmethod
    def crear(cls, id_producto, cantidad, observaciones=None):
        if not id_producto or cantidad <= 0:
            raise ValueError("Producto y cantidad válida son obligatorios")
        return cls(id_producto, cantidad, observaciones)