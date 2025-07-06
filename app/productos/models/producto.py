class Producto:
    def __init__(self, nombre, descripcion, precio_venta, costo, stock, id_farmacia):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_venta = precio_venta
        self.costo = costo
        self.stock = stock
        self.id_farmacia = id_farmacia

    @classmethod
    def crear(cls, nombre, descripcion, precio_venta, costo, stock, id_farmacia):
        if not nombre or precio_venta is None or costo is None or stock is None or id_farmacia is None:
            raise ValueError("Faltan campos obligatorios para crear el producto")
        if precio_venta < 0 or costo < 0 or stock < 0:
            raise ValueError("Precio, costo y stock no pueden ser negativos")
        return cls(
            nombre.strip(),
            descripcion.strip() if descripcion else "",
            float(precio_venta),
            float(costo),
            int(stock),
            int(id_farmacia)
        )