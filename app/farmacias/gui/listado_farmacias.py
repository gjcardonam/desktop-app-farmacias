import tkinter as tk
from tkinter import ttk
from app.farmacias.services.farmacia_service import obtener_todas_las_farmacias
from app.farmacias.gui.editar_farmacia_form import mostrar_formulario_edicion_farmacia
from utils.ui_utils import centrar_ventana

def mostrar_listado_farmacias(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Farmacias")
    ventana.geometry("600x400")
    centrar_ventana(ventana, 600, 400)

    columnas = ("id", "nombre", "nit", "direccion", "telefono")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120)

    def cargar_farmacias():
        for item in tree.get_children():
            tree.delete(item)
        farmacias = obtener_todas_las_farmacias()
        for f in farmacias:
            tree.insert("", "end", values=(f["id"], f["nombre"], f["nit"], f["direccion"], f["telefono"]))

    def on_double_click(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            farmacia_id = int(valores[0])
            mostrar_formulario_edicion_farmacia(root, farmacia_id, cargar_farmacias)

    tree.bind("<Double-1>", on_double_click)

    tree.pack(expand=True, fill="both", padx=10, pady=10)
    cargar_farmacias()