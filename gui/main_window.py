import tkinter as tk
from tkinter import ttk, messagebox
from gui.cliente_form import mostrar_formulario_cliente
from gui.farmacia_form import mostrar_formulario_farmacia
from gui.listado_clientes import mostrar_listado_clientes
from gui.listado_farmacias import mostrar_listado_farmacias
from gui.producto_form import mostrar_formulario_producto
from gui.listado_productos import mostrar_listado_productos
from gui.factura_venta_form import mostrar_formulario_factura
from gui.usuario_form import mostrar_formulario_usuario
from gui.listado_usuarios import mostrar_listado_usuarios


def start_main_window():
    root = tk.Tk()
    root.title("Farmacontable")
    root.geometry("800x600")

    # Menú principal
    menubar = tk.Menu(root)

    # Menú de Usuarios
    usuarios_menu = tk.Menu(menubar, tearoff=0)
    usuarios_menu.add_command(label="Agregar Usuario", command=lambda: mostrar_formulario_usuario(root))
    usuarios_menu.add_command(label="Listar Usuarios", command=lambda: mostrar_listado_usuarios(root))
    menubar.add_cascade(label="Usuarios", menu=usuarios_menu)

    # Menú de Clientes
    clientes_menu = tk.Menu(menubar, tearoff=0)
    clientes_menu.add_command(label="Agregar Cliente", command=lambda: mostrar_formulario_cliente(root))
    clientes_menu.add_command(label="Listar Clientes", command=lambda: mostrar_listado_clientes(root))
    menubar.add_cascade(label="Clientes", menu=clientes_menu)

    # Menú de Farmacias
    farmacias_menu = tk.Menu(menubar, tearoff=0)
    farmacias_menu.add_command(label="Agregar Farmacia", command=lambda: mostrar_formulario_farmacia(root))
    farmacias_menu.add_command(label="Listar Farmacias", command=lambda: mostrar_listado_farmacias(root))
    menubar.add_cascade(label="Farmacias", menu=farmacias_menu)

    # Menú de Productos
    productos_menu = tk.Menu(menubar, tearoff=0)
    productos_menu.add_command(label="Agregar Producto", command=lambda: mostrar_formulario_producto(root))
    productos_menu.add_command(label="Listar Productos", command=lambda: mostrar_listado_productos(root))
    menubar.add_cascade(label="Productos", menu=productos_menu)

    # Menú de Facturas
    ventas_menu = tk.Menu(menubar, tearoff=0)
    ventas_menu.add_command(label="Registrar Factura", command=lambda: mostrar_formulario_factura(root))
    menubar.add_cascade(label="Ventas", menu=ventas_menu)

    root.config(menu=menubar)

    # Bienvenida
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Bienvenido a Farmacontable", font=("Helvetica", 16)).pack(pady=20)

    ttk.Button(frame, text="Agregar Usuario", command=lambda: mostrar_formulario_usuario(root)).pack(pady=5)
    ttk.Button(frame, text="Agregar Cliente", command=lambda: mostrar_formulario_cliente(root)).pack(pady=5)
    ttk.Button(frame, text="Agregar Farmacia", command=lambda: mostrar_formulario_farmacia(root)).pack(pady=5)
    ttk.Button(frame, text="Agregar Producto", command=lambda: mostrar_formulario_producto(root)).pack(pady=5)
    ttk.Button(frame, text="Registrar Factura", command=lambda: mostrar_formulario_factura(root)).pack(pady=5)

    root.mainloop()