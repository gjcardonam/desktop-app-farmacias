import tkinter as tk
from tkinter import ttk
from app.farmacias.services.farmacia_service import obtener_todas_las_farmacias
from app.farmacias.gui.editar_farmacia_form import mostrar_formulario_edicion_farmacia
from utils.ui_utils import centrar_ventana

def mostrar_buscador_farmacias(root):
    ventana = tk.Toplevel(root)
    ventana.title("Buscador de farmacias")
    ventana.geometry("800x400")
    centrar_ventana(ventana, 800, 400)

    tk.Label(ventana, text="Buscar farmacia por nombre:").pack(pady=5)
    entry_busqueda = tk.Entry(ventana, width=50)
    entry_busqueda.pack()

    columnas = ("id", "nombre", "nit", "direccion", "telefono")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=150)

    def cargar_farmacias_filtradas():
        query = entry_busqueda.get().strip().lower()
        tree.delete(*tree.get_children())

        if not query:
            return

        farmacias = obtener_todas_las_farmacias()
        for farmacia in farmacias:
            if query in farmacia["nombre"].lower():
                tree.insert("", "end", values=(
                    farmacia["id"],
                    farmacia["nombre"],
                    farmacia["nit"],
                    farmacia["direccion"],
                    farmacia["telefono"]
                ))

    def on_activate(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            farmacia_id = int(valores[0])
            mostrar_formulario_edicion_farmacia(root, farmacia_id, cargar_farmacias_filtradas)

    tree.bind("<<TreeviewActivate>>", on_activate)

    tk.Button(ventana, text="Buscar", command=cargar_farmacias_filtradas).pack(pady=5)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    cargar_farmacias_filtradas()