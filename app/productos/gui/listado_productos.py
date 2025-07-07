import tkinter as tk
from tkinter import ttk

from app.productos.services.producto_service import obtener_todos_los_productos
from app.productos.gui.editar_producto_form import mostrar_formulario_edicion_producto
from utils.treeview_helpers import bind_treeview_activate
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

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Cargar datos
    def cargar_productos():
        tree.delete(*tree.get_children())      # Limpia en una sola llamada
        for p in obtener_todos_los_productos():
            tree.insert(
                "", "end",
                values=(
                    p["id"],
                    p["nombre"],
                    f"${p['precio_venta']:.2f}",
                    p["stock"],
                    p["farmacia"],
                ),
            )

    # Vincular Treeview al helper
    bind_treeview_activate(
        tree,
        lambda producto_id: mostrar_formulario_edicion_producto(
            root, producto_id, cargar_productos
        )
    )

    cargar_productos()
