import tkinter as tk
from tkinter import ttk
from app.clientes.services.cliente_service import obtener_todos_los_clientes
from app.clientes.gui.editar_cliente_form import mostrar_formulario_edicion_cliente
from utils.ui_utils import centrar_ventana

def mostrar_listado_clientes(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Clientes")
    ventana.geometry("600x400")
    centrar_ventana(ventana, 600, 400)

    columnas = ("id", "nombre", "documento", "telefono")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    def cargar_clientes():
        # Limpiar
        for item in tree.get_children():
            tree.delete(item)
        # Recargar
        clientes = obtener_todos_los_clientes()
        for c in clientes:
            tree.insert("", "end", values=(c["id"], c["nombre"], c["documento"], c["telefono"]))

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    def on_double_click(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            cliente_id = int(valores[0])
            mostrar_formulario_edicion_cliente(root, cliente_id, cargar_clientes)

    tree.bind("<Double-1>", on_double_click)
    cargar_clientes()