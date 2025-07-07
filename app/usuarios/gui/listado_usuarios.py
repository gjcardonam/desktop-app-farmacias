import tkinter as tk
from tkinter import ttk

from app.usuarios.services.usuario_service import obtener_todos_los_usuarios
from app.usuarios.gui.editar_usuario_form import mostrar_formulario_edicion_usuario
from utils.treeview_helpers import bind_treeview_activate
from utils.ui_utils import centrar_ventana


def mostrar_listado_usuarios(root: tk.Tk) -> None:
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Usuarios")
    ventana.geometry("600x400")
    centrar_ventana(ventana, 600, 400)

    columnas = ("id", "nombre", "email")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # ── carga / recarga ────────────────────────────────────────────────
    def cargar_usuarios() -> None:
        tree.delete(*tree.get_children())          # limpia el Treeview
        for u in obtener_todos_los_usuarios():
            tree.insert("", "end", values=(u["id"], u["nombre"], u["email"]))

    # ── vínculo Enter + clic simple (o doble, según tu config global) ──
    bind_treeview_activate(
        tree,
        lambda user_id: mostrar_formulario_edicion_usuario(
            root, user_id, cargar_usuarios
        )
    )

    cargar_usuarios()
