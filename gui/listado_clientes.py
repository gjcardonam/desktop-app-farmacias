import tkinter as tk
from tkinter import ttk
from services.cliente_service import obtener_todos_los_clientes

def mostrar_listado_clientes(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Clientes")
    ventana.geometry("600x400")

    columnas = ("id", "nombre", "documento", "telefono")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    clientes = obtener_todos_los_clientes()
    for c in clientes:
        tree.insert("", "end", values=(c["id"], c["nombre"], c["documento"], c["telefono"]))

    tree.pack(expand=True, fill="both", padx=10, pady=10)