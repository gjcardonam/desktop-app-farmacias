
-- =========================================
-- Script de Creación de Base de Datos
-- Sistema de Contabilidad para Farmacias
-- =========================================

CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    rol VARCHAR(50) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE Farmacia (
    id_farmacia SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    nit VARCHAR(20) UNIQUE NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(30)
);

CREATE TABLE Producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio_venta DECIMAL(10,2) NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    id_farmacia INT REFERENCES Farmacia(id_farmacia)
);

CREATE TABLE Cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    documento VARCHAR(50) UNIQUE NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(30)
);

CREATE TABLE Proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    documento VARCHAR(50) UNIQUE NOT NULL,
    telefono VARCHAR(30),
    email VARCHAR(100)
);

CREATE TABLE FacturaVenta (
    id_factura SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT REFERENCES Cliente(id_cliente),
    id_usuario INT REFERENCES Usuario(id_usuario),
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente'
);

CREATE TABLE DetalleVenta (
    id_detalle SERIAL PRIMARY KEY,
    id_factura INT REFERENCES FacturaVenta(id_factura),
    id_producto INT REFERENCES Producto(id_producto),
    cantidad INT NOT NULL,
    precio_unit DECIMAL(10,2) NOT NULL,
    impuesto DECIMAL(10,2)
);

CREATE TABLE CuentaContable (
    id_cuenta SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    nivel INT
);

CREATE TABLE AsientoContable (
    id_asiento SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    descripcion TEXT,
    id_usuario INT REFERENCES Usuario(id_usuario),
    referencia VARCHAR(100)
);

CREATE TABLE MovimientoContable (
    id_movimiento SERIAL PRIMARY KEY,
    id_asiento INT REFERENCES AsientoContable(id_asiento),
    id_cuenta INT REFERENCES CuentaContable(id_cuenta),
    debe DECIMAL(10,2) DEFAULT 0,
    haber DECIMAL(10,2) DEFAULT 0
);

