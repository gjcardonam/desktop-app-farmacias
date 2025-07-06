import tkinter as tk
from tkinter import ttk
from app.proveedores.services.proveedor_service import obtener_todos_los_proveedores
from utils.ui_utils import centrar_ventana
from app.proveedores.gui.editar_proveedor_form import mostrar_formulario_edicion_proveedor

def mostrar_listado_proveedores(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Proveedores")
    ventana.geometry("700x400")
    centrar_ventana(ventana, 700, 400)

    columnas = ("id", "nombre", "documento", "telefono", "email")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120)

    def cargar():
        for item in tree.get_children():
            tree.delete(item)
        for prov in obtener_todos_los_proveedores():
            tree.insert("", "end", values=(
                prov["id"], prov["nombre"], prov["documento"], prov["telefono"], prov["email"]
            ))

    tree.pack(expand=True, fill="both", padx=10, pady=10)
    cargar()

    def on_double_click(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            proveedor_id = int(valores[0])
            mostrar_formulario_edicion_proveedor(root, proveedor_id, cargar)

    tree.bind("<Double-1>", on_double_click)