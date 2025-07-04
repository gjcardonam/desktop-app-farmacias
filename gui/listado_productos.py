import tkinter as tk
from tkinter import ttk
from services.producto_service import obtener_todos_los_productos

def mostrar_listado_productos(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Productos")
    ventana.geometry("700x400")

    columnas = ("id", "nombre", "precio_venta", "stock", "farmacia")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=130)

    productos = obtener_todos_los_productos()
    for p in productos:
        tree.insert("", "end", values=(
            p["id"], p["nombre"], f"${p['precio_venta']:.2f}", p["stock"], p["farmacia"]
        ))

    tree.pack(expand=True, fill="both", padx=10, pady=10)