import tkinter as tk
from tkinter import ttk
from services.farmacia_service import obtener_todas_las_farmacias

def mostrar_listado_farmacias(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Farmacias")
    ventana.geometry("600x400")

    columnas = ("id", "nombre", "nit", "direccion", "telefono")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120)

    farmacias = obtener_todas_las_farmacias()
    for f in farmacias:
        tree.insert("", "end", values=(f["id"], f["nombre"], f["nit"], f["direccion"], f["telefono"]))

    tree.pack(expand=True, fill="both", padx=10, pady=10)