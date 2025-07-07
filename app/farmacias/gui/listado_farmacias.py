import tkinter as tk
from tkinter import ttk

from app.farmacias.services.farmacia_service import obtener_todas_las_farmacias
from app.farmacias.gui.editar_farmacia_form import mostrar_formulario_edicion_farmacia
from utils.treeview_helpers import bind_treeview_activate
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

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Cargar datos
    def cargar_farmacias():
        tree.delete(*tree.get_children())          # limpia con un solo llamado
        for f in obtener_todas_las_farmacias():
            tree.insert(
                "", "end",
                values=(f["id"], f["nombre"], f["nit"], f["direccion"], f["telefono"])
            )

    # Vincular Treeview al helper (Enter o clic disparan edición)
    bind_treeview_activate(
        tree,
        lambda farmacia_id: mostrar_formulario_edicion_farmacia(
            root, farmacia_id, cargar_farmacias
        )
    )

    cargar_farmacias()
