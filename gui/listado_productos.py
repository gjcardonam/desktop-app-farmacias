import tkinter as tk
from tkinter import ttk
from services.producto_service import obtener_todos_los_productos
from gui.editar_producto_form import mostrar_formulario_edicion_producto
from utils.ui_utils import centrar_ventana

def mostrar_listado_productos(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Productos")
    ventana.geometry("700x400")
    centrar_ventana(ventana, 700, 400)

    columnas = ("id", "nombre", "precio_venta", "stock", "farmacia")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=130)

    def cargar_productos():
        for item in tree.get_children():
            tree.delete(item)
        productos = obtener_todos_los_productos()
        for p in productos:
            tree.insert("", "end", values=(
                p["id"], p["nombre"], f"${p['precio_venta']:.2f}", p["stock"], p["farmacia"]
            ))

    def on_double_click(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            producto_id = int(valores[0])
            mostrar_formulario_edicion_producto(root, producto_id, cargar_productos)

    tree.bind("<Double-1>", on_double_click)

    tree.pack(expand=True, fill="both", padx=10, pady=10)
    cargar_productos()