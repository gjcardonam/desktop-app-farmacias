# models/factura.py

class Factura:
    def __init__(self, id_cliente, productos, id_usuario, total):
        self.id_cliente = id_cliente
        self.productos = productos  # Lista de dicts o DTOs con "precio" y "cantidad"
        self.id_usuario = id_usuario
        self.total = total

    @classmethod
    def crear(cls, id_cliente, productos, id_usuario):
        if not id_cliente or not productos or not id_usuario:
            raise ValueError("Cliente, productos y usuario son obligatorios")
        if not isinstance(productos, list) or len(productos) == 0:
            raise ValueError("Debe haber al menos un producto")

        total = 0
        for p in productos:
            if "precio" not in p or "cantidad" not in p:
                raise ValueError("Cada producto debe tener precio y cantidad")
            if p["precio"] < 0 or p["cantidad"] <= 0:
                raise ValueError("Precio o cantidad inválida")
            total += p["precio"] * p["cantidad"]

        return cls(id_cliente, productos, id_usuario, total)