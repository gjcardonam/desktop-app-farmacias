import tkinter as tk
from tkinter import ttk
from app.proveedores.services.proveedor_service import obtener_todos_los_proveedores
from app.proveedores.gui.editar_proveedor_form import mostrar_formulario_edicion_proveedor
from utils.ui_utils import centrar_ventana

def mostrar_buscador_proveedores(root):
    ventana = tk.Toplevel(root)
    ventana.title("Buscador de proveedors")
    ventana.geometry("800x400")
    centrar_ventana(ventana, 800, 400)

    tk.Label(ventana, text="Buscar proveedor por nombre:").pack(pady=5)
    entry_busqueda = tk.Entry(ventana, width=50)
    entry_busqueda.pack()

    columnas = ("id", "nombre", "documento", "telefono")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=150)

    def cargar_proveedors_filtrados():
        query = entry_busqueda.get().strip().lower()
        tree.delete(*tree.get_children())

        if not query:
            return

        proveedors = obtener_todos_los_proveedores()
        for proveedor in proveedors:
            if query in proveedor["documento"].lower():
                tree.insert("", "end", values=(
                    proveedor["id"],
                    proveedor["nombre"],
                    proveedor["documento"],
                    proveedor["telefono"]
                ))

    def on_activate(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            proveedor_id = int(valores[0])
            mostrar_formulario_edicion_proveedor(root, proveedor_id, cargar_proveedors_filtrados)

    tree.bind("<<TreeviewActivate>>", on_activate)

    tk.Button(ventana, text="Buscar", command=cargar_proveedors_filtrados).pack(pady=5)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    cargar_proveedors_filtrados()