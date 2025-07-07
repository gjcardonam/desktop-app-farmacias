import tkinter as tk
from tkinter import ttk
from app.productos.services.producto_service import obtener_todos_los_productos
from app.productos.gui.editar_producto_form import mostrar_formulario_edicion_producto
from utils.ui_utils import centrar_ventana

def mostrar_buscador_productos(root):
    ventana = tk.Toplevel(root)
    ventana.title("Buscador de Productos")
    ventana.geometry("800x400")
    centrar_ventana(ventana, 800, 400)

    tk.Label(ventana, text="Buscar producto por nombre:").pack(pady=5)
    entry_busqueda = tk.Entry(ventana, width=50)
    entry_busqueda.pack()

    columnas = ("id", "nombre", "descripcion", "precio_venta", "stock")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=150)

    def cargar_productos_filtrados():
        query = entry_busqueda.get().strip().lower()
        tree.delete(*tree.get_children())

        if not query:
            return

        productos = obtener_todos_los_productos()
        for prod in productos:
            if query in prod["nombre"].lower():
                tree.insert("", "end", values=(
                    prod["id"],
                    prod["nombre"],
                    prod["descripcion"],
                    f"${prod['precio_venta']:.2f}",
                    prod["stock"]
                ))

    def on_activate(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            producto_id = int(valores[0])
            mostrar_formulario_edicion_producto(root, producto_id, cargar_productos_filtrados)

    tree.bind("<<TreeviewActivate>>", on_activate)

    tk.Button(ventana, text="Buscar", command=cargar_productos_filtrados).pack(pady=5)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    cargar_productos_filtrados()