import tkinter as tk
from tkinter import ttk

from app.proveedores.services.proveedor_service import obtener_todos_los_proveedores
from app.proveedores.gui.editar_proveedor_form import mostrar_formulario_edicion_proveedor
from utils.treeview_helpers import bind_treeview_activate
from utils.ui_utils import centrar_ventana


def mostrar_listado_proveedores(root: tk.Tk) -> None:
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Proveedores")
    ventana.geometry("700x400")
    centrar_ventana(ventana, 700, 400)

    columnas = ("id", "nombre", "documento", "telefono", "email")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # ── carga / recarga ──────────────────────────────────────────────────
    def cargar() -> None:
        tree.delete(*tree.get_children())          # limpia el Treeview
        for p in obtener_todos_los_proveedores():
            tree.insert(
                "", "end",
                values=(
                    p["id"],
                    p["nombre"],
                    p["documento"],
                    p["telefono"],
                    p["email"],
                ),
            )

    # ── vínculo Enter + clic simple (o doble, según config global) ──────
    bind_treeview_activate(
        tree,
        lambda prov_id: mostrar_formulario_edicion_proveedor(
            root, prov_id, cargar
        )
    )

    cargar()
