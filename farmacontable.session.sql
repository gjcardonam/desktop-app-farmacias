-- =========================================
--  Base de datos:  Cadena de Farmacias  (Versión revisada)
--  Autor:  GPT‑assistant (revisión 2025‑07‑16)
--  Notas clave de la revisión
--    • Se eliminan acentos en identificadores.
--    • Estados y tipos normalizados con ENUMs.
--    • CHECK constraints para rangos y lógica básica.
--    • Columnas FK indexadas explícitamente.
--    • Claves únicas donde procede.
-- =========================================

-- =====================================================
-- 1. ENUMs (PostgreSQL > 9.1)
-- =====================================================
CREATE TYPE estado_solicitud_cot AS ENUM ('Abierta','Cerrada','Cancelada','Expirada');
CREATE TYPE estado_envio_cot     AS ENUM ('Enviada','Respondida','Rechazada','SinRespuesta','Expirada');
CREATE TYPE estado_cotizacion    AS ENUM ('Activa','Rechazada','Aceptada','Expirada');
CREATE TYPE estado_orden_compra  AS ENUM ('Pendiente','Aprobada','Parcial','Cancelada','Cerrada');
CREATE TYPE estado_remision      AS ENUM ('Pendiente','Recibida','Parcial','Rechazada','Anulada');
CREATE TYPE estado_recepcion     AS ENUM ('EnRevision','Parcial','Aprobada','Rechazada');
CREATE TYPE estado_factura       AS ENUM ('Pendiente','Aprobada','Rechazada','Conciliada','Anulada');
CREATE TYPE estado_ingreso       AS ENUM ('Pendiente','Confirmado','Anulado');
CREATE TYPE estado_item_recep    AS ENUM ('Pendiente','Aceptado','Rechazado','Parcial');

-- =====================================================
-- 2. Catálogos
-- =====================================================
CREATE TABLE RolUsuario (
    id_rol         SERIAL PRIMARY KEY,
    nombre         VARCHAR(50) NOT NULL UNIQUE,
    descripcion    TEXT
);

CREATE TABLE UnidadMedida (
    id_unidad      SERIAL PRIMARY KEY,
    codigo         VARCHAR(10) NOT NULL UNIQUE,
    descripcion    VARCHAR(100)
);

CREATE TABLE CategoriaProducto (
    id_categoria   SERIAL PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL UNIQUE,
    descripcion    TEXT
);

CREATE TABLE Laboratorio (
    id_laboratorio SERIAL PRIMARY KEY,
    nombre         VARCHAR(150) NOT NULL UNIQUE,
    pais_origen    VARCHAR(100),
    direccion      VARCHAR(200),
    telefono       VARCHAR(30),
    email          VARCHAR(100)
);

CREATE TABLE MunicipioDepartamento (
    id_municipio   SERIAL PRIMARY KEY,
    departamento   VARCHAR(100) NOT NULL,
    municipio      VARCHAR(100) NOT NULL,
    codigo_dane    VARCHAR(20)
);

CREATE TABLE TipoDocumento (
    id_tipo        SERIAL PRIMARY KEY,
    codigo         VARCHAR(5) NOT NULL UNIQUE,
    descripcion    VARCHAR(100)
);

-- =====================================================
-- 3. Entidades base
-- =====================================================
CREATE TABLE Empresa (
    id_empresa     SERIAL PRIMARY KEY,
    razon_social   VARCHAR(200),
    nit            VARCHAR(20) UNIQUE NOT NULL,
    direccion      VARCHAR(200),
    telefono       VARCHAR(30),
    email          VARCHAR(150)
);

CREATE TABLE Sucursal (
    id_sucursal    SERIAL PRIMARY KEY,
    id_empresa     INT NOT NULL REFERENCES Empresa(id_empresa) ON DELETE RESTRICT,
    nombre         VARCHAR(150) NOT NULL,
    codigo_interno VARCHAR(20),
    direccion      VARCHAR(200),
    telefono       VARCHAR(30),
    id_municipio   INT NOT NULL REFERENCES MunicipioDepartamento(id_municipio) ON DELETE RESTRICT,
    codigo_habilitacion VARCHAR(50)
);
CREATE INDEX idx_sucursal_empresa   ON Sucursal(id_empresa);
CREATE INDEX idx_sucursal_municipio ON Sucursal(id_municipio);

CREATE TABLE Usuario (
    id_usuario     SERIAL PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL,
    email          VARCHAR(150) UNIQUE NOT NULL,
    id_rol         INT NOT NULL REFERENCES RolUsuario(id_rol) ON DELETE RESTRICT,
    password_hash  VARCHAR(255) NOT NULL,
    activo         BOOLEAN DEFAULT TRUE,
    id_sucursal    INT NOT NULL REFERENCES Sucursal(id_sucursal) ON DELETE RESTRICT
);
CREATE INDEX idx_usuario_sucursal ON Usuario(id_sucursal);

CREATE TABLE Cliente (
    id_cliente     SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(200) NOT NULL,
    tipo_documento  VARCHAR(5) NOT NULL,
    numero_documento VARCHAR(30) NOT NULL UNIQUE,
    direccion      VARCHAR(200),
    telefono       VARCHAR(30),
    email          VARCHAR(150),
    tipo_cliente   VARCHAR(50),
    regimen_tributario VARCHAR(50),
    es_responsable_iva BOOLEAN,
    requiere_factura_electronica BOOLEAN,
    activo         BOOLEAN DEFAULT TRUE
);

CREATE TABLE Proveedor (
    id_proveedor   SERIAL PRIMARY KEY,
    nombre_legal   VARCHAR(200) NOT NULL,
    nombre_comercial VARCHAR(200),
    tipo_documento VARCHAR(5) NOT NULL,
    numero_documento VARCHAR(30) NOT NULL UNIQUE,
    direccion      VARCHAR(200),
    telefono       VARCHAR(30),
    email          VARCHAR(150),
    responsable_legal VARCHAR(150),
    regimen_tributario VARCHAR(50),
    tipo_persona   VARCHAR(20),
    activo         BOOLEAN DEFAULT TRUE
);

-- =====================================================
-- 4. Productos y stock
-- =====================================================
CREATE TABLE Producto (
    id_producto    SERIAL PRIMARY KEY,
    nombre         VARCHAR(200) NOT NULL,
    descripcion    TEXT,
    codigo_barras  VARCHAR(50) UNIQUE,
    codigo_interno VARCHAR(50),
    codigo_cum     VARCHAR(50),
    id_unidad_medida INT REFERENCES UnidadMedida(id_unidad) ON DELETE RESTRICT,
    concentracion  VARCHAR(100),
    forma_farmaceutica VARCHAR(50),
    presentacion   VARCHAR(100),
    tipo_producto  VARCHAR(50),
    marca_comercial VARCHAR(100),
    registro_invima VARCHAR(50),
    estado_registro VARCHAR(20),
    requiere_formula BOOLEAN DEFAULT FALSE,
    controlado     BOOLEAN DEFAULT FALSE,
    porcentaje_iva DECIMAL(5,2) DEFAULT 0.0 CHECK (porcentaje_iva BETWEEN 0 AND 100),
    id_categoria   INT REFERENCES CategoriaProducto(id_categoria) ON DELETE SET NULL,
    id_laboratorio INT REFERENCES Laboratorio(id_laboratorio) ON DELETE SET NULL
);

CREATE TABLE ProductoSucursal (
    id_producto_sucursal SERIAL PRIMARY KEY,
    id_producto   INT NOT NULL REFERENCES Producto(id_producto) ON DELETE CASCADE,
    id_sucursal   INT NOT NULL REFERENCES Sucursal(id_sucursal) ON DELETE CASCADE,
    precio_venta  DECIMAL(12,2) NOT NULL,
    costo         DECIMAL(12,2) NOT NULL,
    stock         INT DEFAULT 0 CHECK (stock >= 0),
    stock_minimo  INT DEFAULT 0 CHECK (stock_minimo >= 0),
    stock_maximo  INT DEFAULT 0 CHECK (stock_maximo >= 0),
    activo        BOOLEAN DEFAULT TRUE,
    UNIQUE (id_producto, id_sucursal)
);
CREATE INDEX idx_prod_suc_prod ON ProductoSucursal(id_producto);
CREATE INDEX idx_prod_suc_suc  ON ProductoSucursal(id_sucursal);

CREATE TABLE LoteProductoSucursal (
    id_lote       SERIAL PRIMARY KEY,
    id_producto   INT NOT NULL REFERENCES Producto(id_producto) ON DELETE CASCADE,
    id_sucursal   INT NOT NULL REFERENCES Sucursal(id_sucursal) ON DELETE CASCADE,
    numero_lote   VARCHAR(50) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    cantidad      INT NOT NULL CHECK (cantidad >= 0),
    precio_costo  DECIMAL(12,2),
    precio_venta  DECIMAL(12,2),
    UNIQUE (id_producto, id_sucursal, numero_lote)
);
CREATE INDEX idx_lote_vto ON LoteProductoSucursal(fecha_vencimiento);

-- =====================================================
-- 5. Módulo de Cotizaciones
-- =====================================================
CREATE TABLE SolicitudCotizacion (
    id_solicitud  SERIAL PRIMARY KEY,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_sucursal   INT NOT NULL REFERENCES Sucursal(id_sucursal) ON DELETE RESTRICT,
    id_usuario    INT NOT NULL REFERENCES Usuario(id_usuario)  ON DELETE RESTRICT,
    estado        estado_solicitud_cot DEFAULT 'Abierta',
    observaciones TEXT
);

CREATE TABLE SolicitudCotizacionDetalle (
    id_detalle    SERIAL PRIMARY KEY,
    id_solicitud  INT REFERENCES SolicitudCotizacion(id_solicitud) ON DELETE CASCADE,
    id_producto   INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    cantidad      INT NOT NULL CHECK (cantidad > 0),
    observaciones TEXT
);

CREATE TABLE SolicitudCotizacionProveedor (
    id_envio      SERIAL PRIMARY KEY,
    id_solicitud  INT REFERENCES SolicitudCotizacion(id_solicitud) ON DELETE CASCADE,
    id_proveedor  INT REFERENCES Proveedor(id_proveedor) ON DELETE RESTRICT,
    fecha_envio   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado        estado_envio_cot DEFAULT 'Enviada'
);

CREATE TABLE CotizacionProveedor (
    id_cotizacion SERIAL PRIMARY KEY,
    id_envio      INT NOT NULL REFERENCES SolicitudCotizacionProveedor(id_envio) ON DELETE CASCADE,
    fecha_respuesta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validez_dias  INT,
    condiciones_pago TEXT,
    observaciones TEXT,
    estado        estado_cotizacion DEFAULT 'Activa'
);

CREATE TABLE CotizacionProveedorDetalle (
    id_detalle    SERIAL PRIMARY KEY,
    id_cotizacion INT REFERENCES CotizacionProveedor(id_cotizacion) ON DELETE CASCADE,
    id_producto   INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    cantidad_ofertada INT NOT NULL CHECK (cantidad_ofertada > 0),
    precio_unitario DECIMAL(12,2) NOT NULL CHECK (price_unitario >= 0),
    unidad_alternativa VARCHAR(20),
    producto_equivalente TEXT,
    observaciones TEXT
);

CREATE TABLE HistorialCotizacion (
    id_historial  SERIAL PRIMARY KEY,
    id_cotizacion INT REFERENCES CotizacionProveedor(id_cotizacion) ON DELETE CASCADE,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    comentario    TEXT
);

CREATE TABLE RechazoCotizacion (
    id_rechazo    SERIAL PRIMARY KEY,
    id_cotizacion INT REFERENCES CotizacionProveedor(id_cotizacion) ON DELETE CASCADE,
    motivo        TEXT,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario)
);

-- =====================================================
-- 6. Orden de Compra
-- =====================================================
CREATE TABLE OrdenCompra (
    id_orden      SERIAL PRIMARY KEY,
    numero_orden  VARCHAR(50) UNIQUE,
    id_sucursal   INT REFERENCES Sucursal(id_sucursal) ON DELETE RESTRICT,
    id_proveedor  INT REFERENCES Proveedor(id_proveedor) ON DELETE RESTRICT,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_requerida DATE,
    estado        estado_orden_compra DEFAULT 'Pendiente',
    id_usuario_creador INT REFERENCES Usuario(id_usuario) ON DELETE RESTRICT,
    id_usuario_aprobador INT REFERENCES Usuario(id_usuario),
    observaciones TEXT,
    origen        VARCHAR(20),
    id_cotizacion INT REFERENCES CotizacionProveedor(id_cotizacion) ON DELETE SET NULL
);

CREATE TABLE OrdenCompraDetalle (
    id_detalle    SERIAL PRIMARY KEY,
    id_orden      INT REFERENCES OrdenCompra(id_orden) ON DELETE CASCADE,
    id_producto   INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    cantidad      INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(12,2) NOT NULL,
    porcentaje_iva DECIMAL(5,2) CHECK (porcentaje_iva BETWEEN 0 AND 100),
    observaciones TEXT
);

CREATE TABLE CondicionComercialOrdenCompra (
    id_condicion  SERIAL PRIMARY KEY,
    id_orden      INT REFERENCES OrdenCompra(id_orden) ON DELETE CASCADE,
    tipo          VARCHAR(50),
    valor         TEXT
);

CREATE TABLE AprobacionOrdenCompra (
    id_aprobacion SERIAL PRIMARY KEY,
    id_orden      INT REFERENCES OrdenCompra(id_orden) ON DELETE CASCADE,
    id_usuario    INT REFERENCES Usuario(id_usuario) ON DELETE RESTRICT,
    fecha_aprobacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comentario    TEXT
);

CREATE TABLE HistorialOrdenCompra (
    id_historial  SERIAL PRIMARY KEY,
    id_orden      INT REFERENCES OrdenCompra(id_orden) ON DELETE CASCADE,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    accion        TEXT,
    comentario    TEXT
);

CREATE TABLE DocumentoAdjuntoOrdenCompra (
    id_adjunto    SERIAL PRIMARY KEY,
    id_orden      INT REFERENCES OrdenCompra(id_orden) ON DELETE CASCADE,
    nombre_archivo VARCHAR(255),
    url_archivo   TEXT,
    fecha_subida  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 7. Remisión del Proveedor
-- =====================================================
CREATE TABLE RemisionProveedor (
    id_remision   SERIAL PRIMARY KEY,
    numero_remision VARCHAR(50) NOT NULL,
    id_orden      INT REFERENCES OrdenCompra(id_orden) ON DELETE SET NULL,
    id_proveedor  INT REFERENCES Proveedor(id_proveedor) ON DELETE RESTRICT,
    id_sucursal   INT REFERENCES Sucursal(id_sucursal) ON DELETE RESTRICT,
    fecha_remision DATE NOT NULL,
    fecha_recepcion_estimada DATE,
    estado        estado_remision DEFAULT 'Pendiente',
    observaciones TEXT
);

CREATE TABLE RemisionDetalle (
    id_detalle    SERIAL PRIMARY KEY,
    id_remision   INT REFERENCES RemisionProveedor(id_remision) ON DELETE CASCADE,
    id_producto   INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    cantidad_enviada INT NOT NULL CHECK (cantidad_enviada > 0),
    numero_lote   VARCHAR(50) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    observaciones TEXT
);

CREATE TABLE DiscrepanciaRemision (
    id_discrepancia SERIAL PRIMARY KEY,
    id_detalle    INT REFERENCES RemisionDetalle(id_detalle) ON DELETE CASCADE,
    tipo          VARCHAR(50),
    descripcion   TEXT,
    severidad     VARCHAR(20),
    requiere_accion_correctiva BOOLEAN DEFAULT FALSE
);

CREATE TABLE RechazoRemisionDetalle (
    id_rechazo    SERIAL PRIMARY KEY,
    id_detalle    INT REFERENCES RemisionDetalle(id_detalle) ON DELETE CASCADE,
    motivo        TEXT,
    cantidad_rechazada INT NOT NULL CHECK (cantidad_rechazada > 0),
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario)
);

CREATE TABLE HistorialRemisionProveedor (
    id_historial  SERIAL PRIMARY KEY,
    id_remision   INT REFERENCES RemisionProveedor(id_remision) ON DELETE CASCADE,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    accion        TEXT,
    comentario    TEXT
);

CREATE TABLE DocumentoAdjuntoRemision (
    id_adjunto    SERIAL PRIMARY KEY,
    id_remision   INT REFERENCES RemisionProveedor(id_remision) ON DELETE CASCADE,
    nombre_archivo VARCHAR(255),
    url_archivo   TEXT,
    fecha_subida  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE RemisionProductoEquivalente (
    id_equivalente SERIAL PRIMARY KEY,
    id_detalle    INT REFERENCES RemisionDetalle(id_detalle) ON DELETE CASCADE,
    id_producto_original INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    id_producto_entregado INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    justificacion TEXT
);

-- =====================================================
-- 8. Recepción de Mercancía
-- =====================================================
CREATE TABLE RecepcionCompra (
    id_recepcion  SERIAL PRIMARY KEY,
    id_remision   INT REFERENCES RemisionProveedor(id_remision) ON DELETE SET NULL,
    id_sucursal   INT REFERENCES Sucursal(id_sucursal) ON DELETE RESTRICT,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario_receptor INT REFERENCES Usuario(id_usuario) ON DELETE RESTRICT,
    estado        estado_recepcion DEFAULT 'EnRevision',
    observaciones TEXT
);

CREATE TABLE RecepcionDetalle (
    id_detalle    SERIAL PRIMARY KEY,
    id_recepcion  INT REFERENCES RecepcionCompra(id_recepcion) ON DELETE CASCADE,
    id_producto   INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    numero_lote   VARCHAR(50) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    cantidad_recibida INT NOT NULL CHECK (cantidad_recibida >= 0),
    cantidad_rechazada INT DEFAULT 0 CHECK (cantidad_rechazada >= 0),
    estado_item   estado_item_recep DEFAULT 'Pendiente',
    observaciones TEXT
);

CREATE TABLE ChecklistRecepcion (
    id_check      SERIAL PRIMARY KEY,
    id_recepcion  INT REFERENCES RecepcionCompra(id_recepcion) ON DELETE CASCADE,
    criterio      VARCHAR(100),
    cumple        BOOLEAN,
    comentario    TEXT
);

CREATE TABLE RechazoRecepcionDetalle (
    id_rechazo    SERIAL PRIMARY KEY,
    id_detalle    INT REFERENCES RecepcionDetalle(id_detalle) ON DELETE CASCADE,
    motivo        TEXT,
    cantidad      INT CHECK (cantidad > 0),
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario)
);

CREATE TABLE HistorialRecepcionCompra (
    id_historial  SERIAL PRIMARY KEY,
    id_recepcion  INT REFERENCES RecepcionCompra(id_recepcion) ON DELETE CASCADE,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    accion        TEXT,
    comentario    TEXT
);

CREATE TABLE DocumentoAdjuntoRecepcion (
    id_adjunto    SERIAL PRIMARY KEY,
    id_recepcion  INT REFERENCES RecepcionCompra(id_recepcion) ON DELETE CASCADE,
    nombre_archivo VARCHAR(255),
    url_archivo   TEXT,
    fecha_subida  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 9. Factura del Proveedor
-- =====================================================
CREATE TABLE FacturaCompra (
    id_factura    SERIAL PRIMARY KEY,
    numero_factura VARCHAR(50) NOT NULL,
    id_proveedor  INT REFERENCES Proveedor(id_proveedor) ON DELETE RESTRICT,
    id_sucursal   INT REFERENCES Sucursal(id_sucursal) ON DELETE RESTRICT,
    fecha_emision DATE NOT NULL,
    fecha_recepcion DATE,
    subtotal      DECIMAL(14,2),
    total_iva     DECIMAL(14,2),
    total_descuentos DECIMAL(14,2),
    total_factura DECIMAL(14,2),
    estado        estado_factura DEFAULT 'Pendiente',
    observaciones TEXT,
    CHECK (total_factura = subtotal - total_descuentos + total_iva)
);

CREATE TABLE FacturaCompraDetalle (
    id_detalle    SERIAL PRIMARY KEY,
    id_factura    INT REFERENCES FacturaCompra(id_factura) ON DELETE CASCADE,
    id_producto   INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    cantidad      INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(12,2) NOT NULL,
    porcentaje_iva DECIMAL(5,2) CHECK (porcentaje_iva BETWEEN 0 AND 100),
    descuento_item DECIMAL(12,2) DEFAULT 0,
    total_item    DECIMAL(14,2)
);

CREATE TABLE RelacionFacturaRemision (
    id_relacion   SERIAL PRIMARY KEY,
    id_factura    INT REFERENCES FacturaCompra(id_factura) ON DELETE CASCADE,
    id_remision   INT REFERENCES RemisionProveedor(id_remision) ON DELETE RESTRICT
);

CREATE TABLE RetencionFacturaCompra (
    id_retencion  SERIAL PRIMARY KEY,
    id_factura    INT REFERENCES FacturaCompra(id_factura) ON DELETE CASCADE,
    tipo_retencion VARCHAR(50),
    porcentaje    DECIMAL(5,2) CHECK (porcentaje BETWEEN 0 AND 100),
    valor         DECIMAL(12,2)
);

CREATE TABLE RechazoFacturaCompra (
    id_rechazo    SERIAL PRIMARY KEY,
    id_factura    INT REFERENCES FacturaCompra(id_factura) ON DELETE CASCADE,
    motivo        TEXT,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario)
);

CREATE TABLE HistorialFacturaCompra (
    id_historial  SERIAL PRIMARY KEY,
    id_factura    INT REFERENCES FacturaCompra(id_factura) ON DELETE CASCADE,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    accion        TEXT,
    comentario    TEXT
);

CREATE TABLE DocumentoAdjuntoFacturaCompra (
    id_adjunto    SERIAL PRIMARY KEY,
    id_factura    INT REFERENCES FacturaCompra(id_factura) ON DELETE CASCADE,
    nombre_archivo VARCHAR(255),
    url_archivo   TEXT,
    tipo_archivo  VARCHAR(20),
    fecha_subida  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 10. Ingreso a Inventario
-- =====================================================
CREATE TABLE IngresoInventario (
    id_ingreso    SERIAL PRIMARY KEY,
    id_sucursal   INT REFERENCES Sucursal(id_sucursal) ON DELETE RESTRICT,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_ingreso  VARCHAR(20) NOT NULL, -- Recepcion, Ajuste, Devolucion, Manual
    origen_referencia VARCHAR(100),
    estado        estado_ingreso DEFAULT 'Pendiente',
    observaciones TEXT,
    id_usuario    INT REFERENCES Usuario(id_usuario)
);

CREATE TABLE IngresoInventarioDetalle (
    id_detalle    SERIAL PRIMARY KEY,
    id_ingreso    INT REFERENCES IngresoInventario(id_ingreso) ON DELETE CASCADE,
    id_producto   INT REFERENCES Producto(id_producto) ON DELETE RESTRICT,
    numero_lote   VARCHAR(50) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    cantidad      INT NOT NULL CHECK (cantidad > 0),
    precio_costo  DECIMAL(12,2) NOT NULL,
    id_lote_sucursal INT REFERENCES LoteProductoSucursal(id_lote),
    observaciones TEXT
);

CREATE TABLE MovimientoInventario (
    id_movimiento SERIAL PRIMARY KEY,
    id_ingreso    INT REFERENCES IngresoInventario(id_ingreso) ON DELETE CASCADE,
    tipo_movimiento VARCHAR(30), -- Entrada, Anulacion, Ajuste
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    descripcion   TEXT
);

CREATE TABLE AnulacionIngresoInventario (
    id_anulacion  SERIAL PRIMARY KEY,
    id_ingreso    INT REFERENCES IngresoInventario(id_ingreso) ON DELETE CASCADE,
    motivo        TEXT,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario)
);

CREATE TABLE HistorialIngresoInventario (
    id_historial  SERIAL PRIMARY KEY,
    id_ingreso    INT REFERENCES IngresoInventario(id_ingreso) ON DELETE CASCADE,
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario    INT REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    accion        TEXT,
    comentario    TEXT
);

CREATE TABLE DocumentoAdjuntoIngresoInventario (
    id_adjunto    SERIAL PRIMARY KEY,
    id_ingreso    INT REFERENCES IngresoInventario(id_ingreso) ON DELETE CASCADE,
    nombre_archivo VARCHAR(255),
    url_archivo   TEXT,
    fecha_subida  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 11. Índices adicionales para performance (FKs ya indexados arriba)
-- =====================================================
CREATE INDEX idx_recepcion_det_prod ON RecepcionDetalle(id_producto);
CREATE INDEX idx_fact_proveedor     ON FacturaCompra(id_proveedor);
CREATE INDEX idx_fact_estado        ON FacturaCompra(estado);
CREATE INDEX idx_ingreso_estado     ON IngresoInventario(estado);

-- =====================================================
-- FIN DEL SCRIPT REVISION 2025‑07‑16
-- =====================================================
