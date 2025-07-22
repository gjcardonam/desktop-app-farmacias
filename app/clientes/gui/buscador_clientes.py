import tkinter as tk
from tkinter import ttk
from app.clientes.services.cliente_service import obtener_todos_los_clientes
from app.clientes.gui.editar_cliente_form import mostrar_formulario_edicion_cliente
from utils.ui_utils import centrar_ventana

def mostrar_buscador_clientes(root):
    ventana = tk.Toplevel(root)
    ventana.title("Buscador de clientes")
    ventana.geometry("800x400")
    centrar_ventana(ventana, 800, 400)

    tk.Label(ventana, text="Buscar cliente por nombre:").pack(pady=5)
    entry_busqueda = tk.Entry(ventana, width=50)
    entry_busqueda.pack()

    columnas = ("id", "nombre", "documento", "telefono")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=150)

    def cargar_clientes_filtradas():
        query = entry_busqueda.get().strip().lower()
        tree.delete(*tree.get_children())

        if not query:
            return

        clientes = obtener_todos_los_clientes()
        for cliente in clientes:
            if query in cliente["documento"].lower():
                tree.insert("", "end", values=(
                    cliente["id"],
                    cliente["nombre"],
                    cliente["documento"],
                    cliente["telefono"]
                ))

    def on_activate(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            cliente_id = int(valores[0])
            mostrar_formulario_edicion_cliente(root, cliente_id, cargar_clientes_filtradas)

    tree.bind("<<TreeviewActivate>>", on_activate)

    tk.Button(ventana, text="Buscar", command=cargar_clientes_filtradas).pack(pady=5)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    cargar_clientes_filtradas()