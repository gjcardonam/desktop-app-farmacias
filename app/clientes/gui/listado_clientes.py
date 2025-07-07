import tkinter as tk
from tkinter import ttk

from app.clientes.services.cliente_service import obtener_todos_los_clientes
from app.clientes.gui.editar_cliente_form import mostrar_formulario_edicion_cliente
from utils.treeview_helpers import bind_treeview_activate
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

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    def cargar_clientes():
        # Limpiar contenido actual
        for item in tree.get_children():
            tree.delete(item)
        # Poblar con datos frescos
        for c in obtener_todos_los_clientes():
            tree.insert(
                "", "end",
                values=(c["id"], c["nombre"], c["documento"], c["telefono"])
            )

    # Conecta Treeview al callback global: clic o Enter
    bind_treeview_activate(
        tree,
        lambda cliente_id: mostrar_formulario_edicion_cliente(
            root, cliente_id, cargar_clientes
        )
    )

    cargar_clientes()
